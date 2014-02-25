from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_season_nameA, current_season_nameB

from django.template import Context, loader

import time

class Command(BaseCommand):
    args = '<template_name>'
    help = '''Tries to intelligently render an email template. 
            to all participating schools notifying them of
            the upcoming round's matchups. Currently existing templates:
            next-round-announce\n
            previous-round-results\n'''

    def handle(self, *args, **options):
        seasonA = Season.objects.get(name=current_season_nameA)
        seasonB = Season.objects.get(name=current_season_nameB)

        try: 
            next_roundA = Round.objects.get_next_round(seasonA)
            next_roundB = Round.objects.get_next_round(seasonB)
            previous_roundA = Round.objects.get_previous_round(seasonA)
            previous_roundB = Round.objects.get_previous_round(seasonB)
        except:
            self.stdout.write('Warning: Previous or next round was not found.\n')
        
        unmatched_schoolsA = set(bye.school for bye in Bye.objects.filter(round=next_roundA))
        unmatched_schoolsB = set(bye.school for bye in Bye.objects.filter(round=next_roundB))

        c = Context(locals())
        
        try:
            email_template = args[0]
            t = loader.get_template(email_template)
        except Exception, e:
            print e
            raise CommandError('Email template not found')

        with open('templates/rendered-email', 'w') as f:
            f.write(t.render(c))

        self.stdout.write('Email rendered to templates/rendered-email.\n')
        self.stdout.write('Send this email with ./manage.py send_email\n')
