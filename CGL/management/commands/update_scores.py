from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_season_name

from datetime import date, timedelta

class Command(BaseCommand):
    args = '<Season Name>'
    help = '''Recalculates all player records, match scores, and school records
            for the requested season. Defaults to current season'''

    def update_match_and_schools(self, current_season):
        # reset all scores for this season
        for membership in Membership.objects.all().filter(season=current_season):
            membership.num_wins = 0
            membership.num_losses = 0
            membership.num_ties = 0
            membership.save()
            
        # compute the result of each match, based on games and forfeits
        # at the same time, tally up each school's wins/losses
        for round in current_season.round_set.filter(date__lte=date.today()):
            for m in round.match_set.all():
                score1 = 0
                score2 = 0
                for game in m.game_set.all():
                    if game.winner == 'School1':
                        score1 += 1
                    else:
                        score2 += 1
                for forfeit in m.forfeit_set.all():
                    if forfeit.forfeit == 'School1':
                        score2 += 1
                    else:
                        score1 += 1
                m.score1 = score1
                m.score2 = score2
                m.save()

                mem1 = m.school1.membership_set.get(season=current_season)
                mem2 = m.school2.membership_set.get(season=current_season)
                if m.score1 > m.score2:
                    mem1.num_wins += 1
                    mem2.num_losses += 1
                elif m.score1 < m.score2:
                    mem1.num_losses += 1
                    mem2.num_wins += 1
                else:
                    mem1.num_ties += 1
                    mem2.num_ties += 1
                mem1.save()
                mem2.save()
                
    def update_player_record(self, player):        
        wins = 0
        losses = 0

        # Assume player is inactive until evidence to contrary is found
        player.isActive = False
        
        # player was player 1 of a game
        for game in player.game_school1_player.all():
            if (date.today() - game.match.round.date) < timedelta(days=180):
                player.isActive = True

            if game.winner == 'School1':
                wins += 1
            else:
                losses += 1
        # player was player 2 of a game
        for game in player.game_school2_player.all():
            if (date.today() - game.match.round.date) < timedelta(days=180):
                player.isActive = True

            if game.winner == 'School1':
                losses += 1
            else:
                wins += 1
                
        player.num_wins = wins
        player.num_losses = losses
        player.save()
    
    def handle(self, *args, **options):
        if not args:
            season = Season.objects.get(name=current_season_name)
        else:
            season = Season.objects.get(name=args[0])
        self.stdout.write('Updating %s\n' % (season.name))
        self.update_match_and_schools(season)
        self.stdout.write('%s match records updated\n' % (season.name))
        self.stdout.write('School records updated from match results\n')
        for player in Player.objects.all():
            self.update_player_record(player)
        self.stdout.write('All player records updated\n')
        self.stdout.write('Done!\n')
