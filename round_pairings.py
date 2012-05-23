# Script to create pairings for the latest round
#
# To use, first type in "python manage.py shell" in terminal
# then "execfile('round_pairings.py') from within the shell.
#
# This script only runs if the latest round is currently unpopulated. 

from CGL.models import *
from CGL.settings import current_season_name
import random


def find_matchups(match_matrix, all_id):
    ''' given a symmetric matrix of 0's and 1's, returns a list of
    2-tuples (i,j) drawn from all_id, such that no i and j are repeated, and
    that M_ij = 0 for all tuples'''

    
    success = False
    # Outer loop: tries to find a set of random pairings that work,
    # and starts over if it doesn't.
    while success == False:
        matchups = []
        pool = all_id[:]
        # Inner loop: repeatedly selects a school, and chooses a partner.
        # If it can't find a partner, skip to end of while loop and start over
        while True:
            s1 = pool.pop(random.randint(0,len(pool)-1))

            if not any(match_matrix[s1][s2] == 0 for s2 in pool):
                # No partners found!
                break
            
            for i, s2 in enumerate(pool):
                if match_matrix[s1][s2] == 0:
                    pool.pop(i)
                    matchups.append((s1,s2))
                    break
            if len(pool)<2:
                success = True
                break
    return matchups

if __name__ == "__main__":
    next_round = Round.objects.get_next_round

    if not next_round.match_set.all():
        current_season = Season.objects.get(name=current_season_name)

        all_schools = current_season.schools.all()
        all_matches = Match.objects.filter(round__season = current_season)

        all_id = [school.id for school in all_schools]
        max_id = max(all_id) + 1
        # Store all matches as entries M_ij, where i and j are the school.id
        # If M_ij = 1, then school i and school j have already played.
        # If M_ij = 0, then school i and school j have not played.
        match_matrix = [[0]*max_id for i in range(max_id)]
        
        for match in all_matches:
            i, j = match.school1.id, match.school2.id
            match_matrix[i][j] = 1
            match_matrix[j][i] = 1

        # Returns a list of tuples (i,j), such that all entries M_ij are 0.
        # Also, some rows should be ignored, since there may be gaps in school_id
        all_matchups = find_matchups(match_matrix, all_id)

        for matchup in all_matchups:
            new_match = Match(round = next_round,
                              school1 = School.objects.get(id=matchup[0]),
                              school2 = School.objects.get(id=matchup[1]),
                              )
            new_match.save()
        
    else:
        print "Latest round must be empty; delete any existing matchups and try again"
