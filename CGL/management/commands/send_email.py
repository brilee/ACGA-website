from django.core.management.base import BaseCommand
from CGL.models import *
from CGL.settings import current_season_name

from django.core.mail import send_mail

class Command(BaseCommand):
    args = 'None'
    help = '''Sends out the email at templates/round_email.txt to
            all participating schools in the current season.'''

    def handle(self, *args, **options):
        participating_schools = set(m.school for m in Membership.objects.filter(season__name=current_season_name))
        
        with open('templates/round_email.txt') as f:
            email_contents = f.read()
            
        send_mail('CGL Round this week',
                  email_contents,
                  'cgl.tournament.director@gmail.com',
                  [school.contact_email for school in participating_schools])

        self.stdout.write('Emails sent\n')
