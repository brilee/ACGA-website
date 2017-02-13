from collections import defaultdict
import random

def construct_matrix(existing_matchups):
    m = defaultdict(int)
    for match in existing_matchups:
        m[(match.team1.id, match.team2.id)] += 1
        m[(match.team2.id, match.team1.id)] +=1
    return m

def score_matchups(team_pairings, team_bye, matchup_matrix):
    score = 0
    for team1, team2 in team_pairings:
        # penalty for matching up teams who have played before
        score -= 100 * matchup_matrix[(team1.id, team2.id)]
        # penalty for matching up teams with disparate number of wins
        score -= 5 * (team1.num_wins - team2.num_wins)**2
        # penalty for matching two teams from the same school
        if team1.school == team2.school:
            score -= 250

    if team_bye:
        # penalty for giving team byes more than once
        score -= team_bye.num_byes * 100
        # bonus for giving teams with lots of forfeits a bye
        score += team_bye.num_forfeits * 10

    return score

def make_random_matchup(team_pool):
    team_pool = list(team_pool)
    team_pairings = []
    while len(team_pool) > 1:
        team1 = random.choice(team_pool)
        team_pool.remove(team1)
        team2 = random.choice(team_pool)
        team_pool.remove(team2)
        team_pairings.append((team1, team2))
    if len(team_pool) == 1:
        return team_pairings, team_pool[0]
    else:
        return team_pairings, None

def best_matchup(team_pool, existing_matchups, num_iterations=1000):
    matchup_matrix = construct_matrix(existing_matchups)
    best_score = -10000
    best_pairings, best_bye = None, None
    for i in range(num_iterations):
        team_pairings, team_bye = make_random_matchup(team_pool)
        score = score_matchups(team_pairings, team_bye, matchup_matrix)
        if score > best_score:
            best_score = score
            best_pairings, best_bye = team_pairings, team_bye

    # so that things are returned in some predictable order:
    best_pairings = sorted((tuple(sorted(teams, key=lambda t: t.id)) for teams in best_pairings), key=lambda t: t[0].id)
    return best_pairings, best_bye
