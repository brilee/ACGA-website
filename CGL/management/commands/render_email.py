from django.core.management.base import BaseCommand
from CGL.models import *
from CGL.settings import current_season_name

from django.template import Context, loader

import time

class Command(BaseCommand):
    args = 'None'
    help = '''Renders an email to all participating schools notifying them of
            the upcoming round's matchups. Email template can be found under
            /templates/round-announce-email.html'''

    def handle(self, *args, **options): 
        next_round = Round.objects.get_next_round()
        participating_schools = set(m.school for m in Membership.objects.filter(season__name=current_season_name))
        matched_schools = set(m.school1 for m in next_round.match_set.all()) | set(m.school2 for m in next_round.match_set.all())
        unmatched_school = participating_schools - matched_schools
        if unmatched_school:
            # should be either 0 or 1 schools; turn a set of one into its contents.
            unmatched_school = unmatched_school.pop()
        t = loader.get_template('round-announce-email.html')
        c = Context({'unmatched_school':unmatched_school,
                     'next_round':next_round},)

        with open('templates/round_email.txt', 'w') as f:
            f.write(t.render(c))

        self.stdout.write('Email rendered to templates/round_email.txt.\n')
        self.stdout.write('Send this email with ./manage.py send_email.\n')
