from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_seasons as current_season_names

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
        try:
            current_seasons = [Season.objects.get(name=s) for s in current_season_names]
            previous_round_date = Round.objects.get_previous_round().date
            next_round_date = Round.objects.get_next_round().date
        except Exception, e:
            self.stdout.write('Warning: Couldn\'t find previous or next round date.')
        c = Context(locals())
        
        try:
            email_template = args[0]
            t = loader.get_template(email_template)
        except Exception, e:
            self.stdout.write(str(e))
            raise CommandError('Email template not found')

        with open('templates/rendered-email', 'w') as f:
            f.write(t.render(c))

        self.stdout.write('Email rendered to templates/rendered-email.\n')
        self.stdout.write('Send this email with ./manage.py send_email\n')
