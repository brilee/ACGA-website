from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_season_nameA, current_season_nameB

from django.template import Context, loader

import time

class Command(BaseCommand):
    args = '<template_name>'
    help = '''Tries to intelligently render an email template. to all participating schools notifying them of
            the upcoming round's matchups. Currently existing templates:
            next-round-announce\n
            previous-round-results\n'''

    def handle(self, *args, **options):
        memberships = (Membership.objects.filter(season__name=current_season_nameA) |
                       Membership.objects.filter(season__name=current_season_nameB))
                       
        participating_schoolsA = set(m.school for m in Membership.objects.filter(season__name=current_season_nameA) if m.still_participating)
        participating_schoolsB = set(m.school for m in Membership.objects.filter(season__name=current_season_nameB) if m.still_participating)
        try: 
            next_roundA = Round.objects.get_next_round(current_season_nameA)
            next_roundB = Round.objects.get_next_round(current_season_nameB)
            matched_schoolsA = set(m.school1 for m in next_roundA.match_set.all()) | set(m.school2 for m in next_roundA.match_set.all())
            matched_schoolsB = set(m.school1 for m in next_roundB.match_set.all()) | set(m.school2 for m in next_roundB.match_set.all())
            unmatched_schoolA = participating_schoolsA - matched_schoolsA
            unmatched_schoolB = participating_schoolsB - matched_schoolsB
            if unmatched_schoolA:
                # should be either 0 or 1 schools; turn a set of one into its contents.
                unmatched_schoolA = unmatched_schoolA.pop()
            if unmatched_schoolB:
                # should be either 0 or 1 schools; turn a set of one into its contents.
                unmatched_schoolB = unmatched_schoolB.pop()

        except AttributeError:
            self.stdout.write('Warning: No next round exists.\n')        

        try:
            previous_roundA = Round.objects.get_previous_round(current_season_nameA)
            previous_roundB = Round.objects.get_previous_round(current_season_nameB)
        except IndexError:
            self.stdout.write('Warning: no previous round exists.\n')
        
        c = Context(locals())
        
        try:
            email_template = args[0]
            t = loader.get_template(email_template)
        except:
            raise CommandError('Email template not found')

        with open('templates/rendered-email', 'w') as f:
            f.write(t.render(c))

        self.stdout.write('Email rendered to templates/rendered-email.\n')
        self.stdout.write('Send this email with ./manage.py send_email\n')
