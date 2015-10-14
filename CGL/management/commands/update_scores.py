from django.core.management.base import BaseCommand
from CGL.models import Team, Season, School, Player
from CGL.settings import current_seasons

from datetime import date, timedelta

class Command(BaseCommand):
    args = '<Season Name>'
    help = '''Recalculates all player records, match scores, and school records
            for the requested season. Defaults to current season'''

    def update_match_and_schools(self, season):
        # reset all scores for this season; recompute from scratch.
        Team.objects.filter(season=season).update(
            num_wins=0,
            num_losses=0,
            num_ties=0,
            num_byes=0,
            num_forfeits=0
        )
            
        # compute the result of each match, based on games and forfeits
        # at the same time, tally up each school's wins/losses
        all_rounds = season.round_set.filter(date__lte=date.today())
        for round in all_rounds:
            for match in round.match_set.all():
                m = match
                
                # Clear previously calculated match record
                m.score1 = 0
                m.score2 = 0

                # Figure out who won the match. Make note of forfeits.
                for game in m.game_set.all():
                    if game.winner == game.team1_player:
                        m.score1 += 1
                    else:
                        m.score2 += 1
                for forfeit in m.forfeit_set.all():
                    if forfeit.team1_noshow and not forfeit.team2_noshow:
                        m.score2 += 1
                    elif forfeit.team2_noshow and not forfeit.team1_noshow:
                        m.score1 += 1
                m.save()


                if m.is_exhibition:
                    # shortcircuit here. don't want to count exhibition matches
                    # towards season results.
                    continue

                # Update the school's scores based on match result
                for forfeit in m.forfeit_set.all():
                    if forfeit.team1_noshow:
                        m.team1.num_forfeits += 1
                    if forfeit.team2_noshow:
                        m.team2.num_forfeits += 1
                if m.score1 > m.score2:
                    m.team1.num_wins += 1
                    m.team2.num_losses += 1
                elif m.score1 < m.score2:
                    m.team1.num_losses += 1
                    m.team2.num_wins += 1
                else:
                    m.team1.num_ties += 1
                    m.team2.num_ties += 1
                m.team1.save()
                m.team2.save()
        # Every team gets a bye for not having played in a round
        # even if they joined the CGL late; this way we can bias
        # newcomers to always getting paired up. By recalculating
        # this value, it's one less source of non-idempotency when
        # creating matchups + byes each round.
        num_rounds = len(all_rounds)
        for team in Team.objects.filter(season=season):
            team.num_byes = num_rounds - team.num_wins - team.num_losses - team.num_ties
            team.save()
                
    def update_player_record(self, player):  
        player.num_wins = 0
        player.num_losses = 0

        # Assume player is inactive until evidence to contrary is found
        player.isActive = False

        for game in player.game_set():
            if (date.today() - game.match.round.date) < timedelta(days=180):
                player.isActive = True
            if game.winner == player:
                player.num_wins += 1
            else:
                player.num_losses += 1

        player.save()

    def update_school_activeness(self):
        School.objects.all().update(inCGL=False)
        seasons = Season.objects.filter(name__in=current_seasons)
        current_schools = set([school for season in seasons for school in season.schools.all()])
        all_schools = School.objects.all()
        for school in all_schools:
            school.inCGL = school in current_schools
            school.save()

    def handle(self, *args, **options):
        if not args:
            self.stdout.write('No season names provided. Defaulting to %s\n' % current_seasons)
            seasons = [Season.objects.get(name=s) for s in current_seasons]
        else:
            seasons = [Season.objects.get(name=arg) for arg in args]
        for season in seasons:
            self.stdout.write('Updating %s\n' % (season.name))
            self.update_match_and_schools(season)
            self.stdout.write('%s match records updated\n' % (season.name))
            self.stdout.write('School records updated from match results\n')
        self.stdout.write('Updating player records\n')
        for player in Player.objects.all():
            self.update_player_record(player)
        self.stdout.write('All player records updated\n')
        self.update_school_activeness()
        self.stdout.write('Updated school inCGL active status\n')
        self.stdout.write('Done!\n')

