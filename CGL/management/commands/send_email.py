from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_season_name

from django.core.mail import send_mail

class Command(BaseCommand):
    args = '<template_name>'
    help = '''Sends out a rendered email.'''

    def handle(self, *args, **options):
        participating_schools = set(m.school for m in Membership.objects.filter(season__name=current_season_name))

        try:
            f = open('templates/rendered-email')
            subject_line = f.readline().strip()[8:] # remove "Subject:"
            email_contents = f.read()
        except IOError:
            raise CommandError('Rendered email not found!')
        finally:
            f.close()

        send_mail(subject_line,
                  email_contents,
                  'cgl.tournament.director@gmail.com',
                  ([school.contact_email for school in participating_schools] +
                  [player.contact_email for school in participating_schools
                                        for player in school.player_set.all()
                                        if (player.contact_email and player.receiveSpam)]))

        self.stdout.write('Emails sent\n')
