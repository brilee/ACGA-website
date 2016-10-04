from CGL.models import Season, SCHOOL1

for s in Season.objects.all():
    teams = s.team_set.all()
    rosters = {team.id : set() for team in teams}
    for round in s.round_set.all():
        for match in round.match_set.all():
            for game in match.game_set.all():
                if game.white_school == SCHOOL1:
                    game.match.team1.players.add(game.white_player)
                    game.match.team2.players.add(game.black_player)
                else:
                    game.match.team1.players.add(game.black_player)
                    game.match.team2.players.add(game.white_player)
    for t in teams:
        t.save()

