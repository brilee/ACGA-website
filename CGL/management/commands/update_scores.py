from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_seasons, current_ladder_season

from datetime import date, timedelta

class Command(BaseCommand):
    args = '<Season Name>'
    help = '''Recalculates all player records, match scores, and school records
            for the requested season. Defaults to current season'''

    def update_match_and_schools(self, season):
        # reset all scores for this season; recompute from scratch.
        for team in Membership.objects.all().filter(season=season):
            team.num_wins = 0
            team.num_losses = 0
            team.num_ties = 0
            team.num_byes = 0
            team.num_forfeits = 0
            team.save()
            
        # compute the result of each match, based on games and forfeits
        # at the same time, tally up each school's wins/losses
        for round in season.round_set.filter(date__lte=date.today()):
            for b in round.bye_set.all():
                b.team.num_byes += 1
                b.team.save()

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

        for game in player.laddergame_set():
            if game.season.name == current_ladder_season:
                player.isActive = True
            if game.winner == player:
                player.num_wins += 1
            else:
                player.num_losses += 1

        player.save()

    def update_school_activeness(self):
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
        self.stdout.write('Updated school inCGL active status')
        self.stdout.write('Done!\n')

