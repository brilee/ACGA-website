from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_season_name
import random
import datetime

class Command(BaseCommand):
    args = 'None'
    help = '''Creates completely random match pairings for the first round
            that has not happened yet, as judged by today's date'''
    
    def find_matchups(self, match_matrix, all_id):
        ''' match_matrix is defined by M_ij = 1 if schools have already played.
        all_id 
        Returns a set of matchups (i,j) drawn from all_id, such that M_ij = 0
        Algorithm is probabilistic, with chance of success going down as
        constraints are added.

        Algorithm prioritizes schools with fewest forfeits, and works thus:

        1) Take all unmatched schools, sorted by num_forfeits
        2) while len(unmatched_schools) > 1: take first unmatched school and
            pair them up with a random school that they have not played yet.
        3) If we run into a dead end where the last two unmatched schools
            have already played each other: trash all progress and start from (2)
        '''

        success = False
        # Outer loop: repeatedly starts over from scratch until
        # inner loop exits with success == True.
        while success == False:
            matchups = []
            pool = all_id[:]

            while True:
                s1 = pool.pop(0)

                possible_matches = [s for s in pool if match_matrix[s1][s] == 0]

                if not possible_matches:
                    break

                s2 = random.choice(possible_matches)
                pool.remove(s2)
                matchups.append((s1,s2))

                if len(pool)<2:
                    success = True
                    break
        return matchups

    def handle(self, *args, **options):
        next_round = Round.objects.get_next_round()
        if not next_round:
            raise CommandError('No upcoming round. Create a round first')
            
        current_season = Season.objects.get(name=current_season_name)

        # Only retrieves schools that are participating in this season
        # and that have not withdrawn from play.
        all_schools = current_season.schools.filter(membership__still_participating = True)

        if len(all_schools) < 2:
            raise CommandError('Fewer than two schools are registered for the season')

        # This allows for manual matching of schools. Algorithm will then
        # ignore manually matched schools.
        existing_matches = next_round.match_set.all()
        matched_schools = ([m.school1.id for m in existing_matches] +
                           [m.school2.id for m in existing_matches])
        unmatched_schools = all_schools.exclude(id__in=matched_schools)

        # Sort schools by number of forfeits. This ensures that schools with
        # fewest forfeits get matched up consistently, whereas schools with
        # many forfeits are more likely to be sat out.
        def get_forfeits(school, season):
            m = Membership.objects.get(season=season, school=school)
            return m.num_forfeits
        unmatched_schools = sorted(unmatched_schools, key=lambda s: get_forfeits(s, current_season))
        
        # Find existing matches, so that we don't match up two schools again.
        # This also select matches that are prescheduled for the future.
        # This is desirable since if we want to match two schools in the future,
        # it wouldn't do to match them up now.
        existing_matches = Match.objects.filter(round__season = current_season)
        
        # We index each school by school.id
        # Store all matches as entries in an adjacency matrix.
        # If M_ij = 1, then school i and school j have already played.
        # If M_ij = 0, then school i and school j have not played.
        # Adj matrix is inefficient since our matches are pretty sparse.
        # Since we don't have that many schools yet, shouldn't matter.
        # Might have to rework when we get bigger (>100 schools?)
        
        # all_id is the requested list of IDs to be matched.
        # This excludes already-matched schools and IDs corresponding to
        # nonexistent schools, for example if a school was deleted at some point.
        all_id = [school.id for school in unmatched_schools]
        max_id = max(school.id for school in all_schools) + 1
        match_matrix = [[0]*max_id for i in range(max_id)]
        
        for match in existing_matches:
            i, j = match.school1.id, match.school2.id
            match_matrix[i][j] = 1
            match_matrix[j][i] = 1

        while True:
            # See algorithm description above.
            all_matchups = self.find_matchups(match_matrix, all_id)
            unmatched = unmatched_schools[:]
            
            for matchup in all_matchups:
                school1 = School.objects.get(id=matchup[0])
                school2 = School.objects.get(id=matchup[1])
                self.stdout.write('%s vs. %s\n' % (school1, school2))
                unmatched.remove(school1)
                unmatched.remove(school2)
                
            if unmatched:
                self.stdout.write('%s has a bye this round\n' % unmatched)
                
            finalize = ''
            while finalize not in ('Y', 'N', 'quit'):
                finalize = raw_input('Do these matchups look okay? (Y/N/quit)\n')
            if finalize == 'Y':
                # Unpack results and add to database
                for matchup in all_matchups:
                    new_match = Match(round = next_round,
                              school1 = School.objects.get(id=matchup[0]),
                              school2 = School.objects.get(id=matchup[1]),
                              )
                    new_match.save()
                break
            if finalize == 'quit':
                raise CommandError('Exiting without creating matchups')
        self.stdout.write('Matchups created for round on %s\n' % next_round.date)
        
