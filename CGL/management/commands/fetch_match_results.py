from optparse import make_option
from django.core.management.base import BaseCommand

from kgs.scrape_games import get_KGS_games, filter_likely_games, download_gamefile
from CGL.settings import current_seasons
from CGL.models import Season, Round, SCHOOL1, SCHOOL2, Player, Game

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--season', dest='season', default=None, help="Season name. Leave blank to default to current season."),
        make_option('--round', dest='round', default=0, help="Round number. Leave blank to default to most recent round")
    )
    args = '--season="Season Name" --round=3'
    help = '''Fetches match results from KGS for the most recent round
            as judged by today's date'''

    def handle(self, *args, **options):
        if options['season']:
            season = Season.objects.get(name=options['season'])
        else:
            season = Season.objects.get(name=current_seasons[0])
        if options['round']:
            round = Round.objects.get(season=season, round_number=int(options['round']))
        else:
            round = season.round_set.get_previous_round()

        year = round.date.year
        month = round.date.month
        for match in round.match_set.all():
            school1 = match.team1.school
            school2 = match.team2.school
            team1_player = Player.objects.get(name="Unknown Player", school=school1)
            team2_player = Player.objects.get(name="Unknown Player", school=school2)
            for i in "123":
                school1_username = school1.KGS_name + i
                school2_username = school2.KGS_name + i
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

                    gamefile = download_gamefile(kgs_game)
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
                    self.stdout.write("Couldn't find game for %s vs %s board %s" % (school1.name, school2.name, i))

