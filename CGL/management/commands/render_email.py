from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_season_name

from django.template import Context, loader

import time

class Command(BaseCommand):
    args = '<template_name>'
    help = '''Tries to intelligently render an email template. to all participating schools notifying them of
            the upcoming round's matchups. Currently existing templates:
            next-round-announce\n
            previous-round-results\n'''

    def handle(self, *args, **options):
        participating_schools = set(m.school for m in Membership.objects.filter(season__name=current_season_name) if m.still_participating)

        try: 
            next_round = Round.objects.get_next_round()
            matched_schools = set(m.school1 for m in next_round.match_set.all()) | set(m.school2 for m in next_round.match_set.all())
            unmatched_school = participating_schools - matched_schools
            if unmatched_school:
                # should be either 0 or 1 schools; turn a set of one into its contents.
                unmatched_school = unmatched_school.pop()

        except AttributeError:
            self.stdout.write('Warning: No next round exists.\n')        

        try:
            previous_round = Round.objects.get_previous_round()
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
