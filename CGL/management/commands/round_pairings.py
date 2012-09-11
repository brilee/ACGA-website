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
        '''

        success = False
        # Outer loop: tries to find a set of random pairings that work,
        # and starts over if it doesn't.
        while success == False:
            matchups = []
            pool = all_id[:]
            # Select a random school. Find the first valid partner.
            # Check those schools off [by removing from pool]. Repeat.
            # If at any point a school cannot be matched, start over.
            while True:
                # Select random school
                s1 = pool.pop(random.randint(0,len(pool)-1))

                if not any(match_matrix[s1][s2] == 0 for s2 in pool):
                    # No valid partner found
                    break
                
                for i, s2 in enumerate(pool):
                    # Find the first matching school, then remove from pool
                    if match_matrix[s1][s2] == 0:
                        pool.pop(i)
                        matchups.append((s1,s2))
                        break
                if len(pool)<2:
                    # We've matched all but 0 or 1 of the schools, so we're done.
                    # Schools with more constraints is more likely to be left unmatched.
                    success = True
                    break
        return matchups

    def handle(self, *args, **options):
        next_round = Round.objects.get_next_round()
        if not next_round:
            raise CommandError('No upcoming round. Create a round first')
            
        current_season = Season.objects.get(name=current_season_name)

        # Only retrieves the schools signed up for current season.
        all_schools = current_season.schools.all()

        if len(all_schools) < 2:
            raise CommandError('Fewer than two schools are registered for the season')

        existing_matches = next_round.match_set.all()
        matched_schools = ([m.school1.id for m in existing_matches] +
                           [m.school2.id for m in existing_matches])
        unmatched_schools = all_schools.exclude(id__in=matched_schools)

        # Note - this also select matches that are prescheduled for the future.
        # This is desirable since if we want to match two schools in the future,
        # it wouldn't do to match them up now.
        all_matches = Match.objects.filter(round__season = current_season)
        
        # We index each school by school.id
        # Store all matches as entries in an adjacency matrix.
        # If M_ij = 1, then school i and school j have already played.
        # If M_ij = 0, then school i and school j have not played.
        # Adj matrix is super inefficient since our matches are pretty sparse,
        # but well.. we don't have that many schools, yet. Might have to rework
        # when we get bigger (>100 schools?)
        
        # all_id is the requested list of IDs to be matched.
        # This excludes already-matched schools and IDs corresponding to
        # nonexistent schools, for example if a school was deleted at some point.
        all_id = [school.id for school in unmatched_schools]
        max_id = max(school.id for school in all_schools) + 1
        match_matrix = [[0]*max_id for i in range(max_id)]
        
        for match in all_matches:
            i, j = match.school1.id, match.school2.id
            match_matrix[i][j] = 1
            match_matrix[j][i] = 1

        # See algorithm description above.
        all_matchups = self.find_matchups(match_matrix, all_id)

        # Unpack the results and create matches in database.
        for matchup in all_matchups:
            new_match = Match(round = next_round,
                              school1 = School.objects.get(id=matchup[0]),
                              school2 = School.objects.get(id=matchup[1]),
                              )
            new_match.save()
        self.stdout.write('Matchups created for round on %s\n' % next_round.date)
        
