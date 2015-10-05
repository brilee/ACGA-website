from django.core.management.base import BaseCommand

from kgs.scrape_games import get_KGS_games, filter_likely_games, download_gamefile
from CGL.settings import current_seasons
from CGL.models import Season, SCHOOL1, SCHOOL2, Player, Game

class Command(BaseCommand):
    help = '''Fetches match results from KGS for the most recent round
            as judged by today's date'''

    def handle(self, *args, **options):
        season = Season.objects.get(name=current_seasons[0])
        round = season.round_set.get_previous_round()

        year = round.date.year
        month = round.date.month
        for match in round.match_set.all():
            school1 = match.team1.school
            school2 = match.team2.school
            self.stderr.write("Handling %s vs %s\n" % (school1.name, school2.name))
            team1_player = Player.objects.get(name="Unknown Player", school=school1)
            team2_player = Player.objects.get(name="Unknown Player", school=school2)
            for i in "123":
                existing_game = Game.objects.filter(match=match, board=i)
                if existing_game:
                    self.stderr.write("Board %s already exists\n" % i)
                    continue
                self.stderr.write("Fetching game info from KGS\n")
                school1_username = (school1.KGS_name + i).lower()
                school2_username = (school2.KGS_name + i).lower()
                all_games = get_KGS_games(school1_username, year, month)
                likely_games = filter(
                    filter_likely_games(
                        school1_username, school2_username, date=round.date),
                    all_games
                )
                if likely_games:
                    kgs_game = likely_games[0]
                    if kgs_game.white == school1_username:
                        white_school = SCHOOL1
                        white_player = team1_player
                        black_player = team2_player
                    else:
                        white_school = SCHOOL2
                        white_player = team2_player
                        black_player = team1_player

                    gamefile = download_gamefile(kgs_game.sgf_url)
                    g = Game(
                        white_player=white_player,
                        black_player=black_player,
                        match=match,
                        board=i,
                        white_school=white_school,
                        gamefile=gamefile,
                    )
                    g.save()
                else:
                    self.stderr.write("Couldn't find game for %s vs %s board %s\n" % (school1.name, school2.name, i))

