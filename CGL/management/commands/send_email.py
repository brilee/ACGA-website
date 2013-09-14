from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from CGL.models import *
from CGL.settings import current_season_name


from django.core.mail import send_mail

class Command(BaseCommand):
    args = '<template_name>'
    help = '''Sends out a rendered email.'''
    option_list = BaseCommand.option_list + (make_option('--fake', default=False, help='Don\'t actually send the email. Default is false'),)

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

        recipients = ([school.contact_email for school in participating_schools] +
                      [player.User.email for school in participating_schools
                                         for player in school.player_set.all()
                                         if (player.User and player.receiveSpam)]))
        if options['fake']: 
            self.stdout.write('You would have sent an email with:')
            self.stdout.write('Subject: %s' % subject_line)
            self.stdout.write('Contents: %s' % email_contents)
            self.stdout.write('Recipients:' + ', '.join(recipients))
        else:
            send_mail(subject_line,
                      email_contents,
                      'cgl.tournament.director@gmail.com',
                      recipients,)
            self.stdout.write('Emails sent\n')


