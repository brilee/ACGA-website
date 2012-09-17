from django.core.management.base import BaseCommand
from CGL.models import *
from CGL.settings import current_season_name

from django.template import Context, loader
from django.core.mail import send_mail

class Command(BaseCommand):
    args = 'None'
    help = '''Sends an email to all participating schools notifying them of
            the upcoming round's matchups. Email template can be found under
            /templates/round-announce-email.html'''

    def handle(self, *args, **options):
        next_round = Round.objects.get_next_round()
        participating_schools = set(m.school for m in Membership.objects.filter(season__name=current_season_name))
        matched_schools = set(m.school1 for m in next_round.match_set.all()) | set(m.school2 for m in next_round.match_set.all())
        unmatched_school = participating_schools - matched_schools

        t = loader.get_template('round-announce-email.html')
        c = Context({'unmatched_school':unmatched_school, 'next_round':next_round},)

# for debugging... wouldn't want to repeatedly send out emails.
#        self.stdout.write(t.render(c))
#        for school in participating_schools:
#            self.stdout.write(school.contact_email)
            
        send_mail('CGL Round this week',
                  t.render(c),
                  'cgl.tournament.director@gmail.com',
                  [school.contact_email for school in participating_schools])
