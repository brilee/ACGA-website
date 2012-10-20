from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_season_name

from django.core.mail import send_mail

class Command(BaseCommand):
    args = '<template_name>'
    help = '''Sends out a rendered email.
            See ./manage.py render_email for details'''

    def handle(self, *args, **options):
        participating_schools = set(m.school for m in Membership.objects.filter(season__name=current_season_name))

        try:
            email_template = args[0]
            f = open('templates/rendered-%s' % email_template
            email_contents = f.read()
        except IOError:
            raise CommandError('Rendered email not found!')
        finally:
            f.close()

        subjects = {'next-round-announce': "[CGL] Next round: pairings announced",
                    'previous-round-results': "[CGL] Previous round games uploaded!"
        
        send_mail(subjects[email_template]
                  email_contents,
                  'cgl.tournament.director@gmail.com',
                  [school.contact_email for school in participating_schools])

        self.stdout.write('Emails sent\n')
