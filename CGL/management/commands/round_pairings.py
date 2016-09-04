import itertools
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from CGL.models import CurrentSeasons, Season, Round, Match, Team
from CGL.matchmaking import best_matchup

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--season', dest='season', default=None, help="Season name. Leave blank to default to current season."),
        make_option('--round', dest='round', default=0, help="Round number. Leave blank to default to next round")
    )
    args = '--season="Season Name" --round=3'
    help = '''Creates completely random match pairings for the first round
            that has not happened yet, as judged by today's date'''

    def handle(self, *args, **options):
        if options['season']:
            season = Season.objects.get(name=options['season'])
        else:
            season = CurrentSeasons.objects.get()[0]
        if options['round']:
            round = Round.objects.get(season=season, round_number=int(options['round']))
        else:
            round = season.round_set.get_next_round()

        all_teams = set(Team.objects.filter(season=season, still_participating=True))
        already_matched = set(itertools.chain(*[(match.team1.id, match.team2.id) for match in round.match_set.all()]))
        team_pool = [t for t in all_teams if t.id not in already_matched]

        if len(team_pool) < 2:
            raise CommandError("Not enough schools to do a pairing for round %s" % round.round_number)

        existing_matchups = Match.objects.filter(round__season=season)

        self.stdout.write("Making matches for %s, round %s on %s" % (season, round.round_number, round.date))
        team_pairings, team_bye = best_matchup(team_pool, existing_matchups)
        for pairing in team_pairings:
            self.stdout.write('%s vs. %s\n' % pairing)
        if team_bye:
            self.stdout.write('%s has a bye this round\n' % team_bye)
        self.stdout.write('Registering matchups!\n')
        for pairing in team_pairings:
            Match.objects.create(round=round, team1=pairing[0], team2=pairing[1])

