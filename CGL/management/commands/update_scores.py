from django.core.management.base import BaseCommand, CommandError
from CGL.models import *

from datetime import date, timedelta

class Command(BaseCommand):
    args = '<Season Name>'
    help = '''Recalculates all player records, match scores, and school records
            for the requested season. Defaults to current season'''

    def update_match_and_schools(self, current_season):
        # reset all scores for this season; recompute from scratch.
        for membership in Membership.objects.all().filter(season=current_season):
            membership.num_wins = 0
            membership.num_losses = 0
            membership.num_ties = 0
            membership.num_byes = 0
            membership.num_forfeits = 0
            membership.save()
            
        # compute the result of each match, based on games and forfeits
        # at the same time, tally up each school's wins/losses
        for round in current_season.round_set.filter(date__lte=date.today()):
            for b in round.bye_set.all():
                mem = b.school.membership_set.get(season=current_season)
                mem.num_byes += 1
                mem.save()

            for match in round.match_set.all():
                m = match
                
                mem1 = m.school1.membership_set.get(season=current_season)
                mem2 = m.school2.membership_set.get(season=current_season)
                
                # Clear previously calculated match record
                m.score1 = 0
                m.score2 = 0

                # Figure out who won the match. Make note of forfeits.
                for game in m.game_set.all():
                    if game.winning_school == 'School1':
                        m.score1 += 1
                    else:
                        m.score2 += 1
                for forfeit in m.forfeit_set.all():
                    if forfeit.school1_noshow and forfeit.school2_noshow:
                        mem1.num_forfeits += 1
                        mem2.num_forfeits += 1
                    elif forfeit.school1_noshow and not forfeit.school2_noshow:
                        m.score2 += 1
                        mem1.num_forfeits += 1
                    elif forfeit.school2_noshow and not forfeit.school1_noshow:
                        m.score1 += 1
                        mem2.num_forfeits += 1
                m.save()

                # Update the school's scores based on match result
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
        player.num_wins = 0
        player.num_losses = 0

        # Assume player is inactive until evidence to contrary is found
        player.isActive = False

        for game in player.game_set():
            if (date.today() - game.match.round.date) < timedelta(days=180):
                player.isActive = True
            if game.winner() == player:
                player.num_wins += 1
            else:
                player.num_losses += 1
        player.save()
    
    def handle(self, *args, **options):
        if not args:
            raise CommandError('Must provide a season name!')
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
