import time
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.template import Context, loader

from CGL.models import *
from CGL.settings import current_seasons as current_season_names

class Command(BaseCommand):
    args = '<template_name>'
    help = '''Tries to intelligently render an email template. 
            to all participating schools notifying them of
            the upcoming round's matchups. Currently existing templates:
            next-round-announce\n
            previous-round-results\n'''

    option_list = BaseCommand.option_list + (
        make_option('--all', default=False, help='Send to all schools, regardless of participation in season'),
    )

    def handle(self, *args, **options):
        try:
            current_seasons = [Season.objects.get(name=s) for s in current_season_names]
            previous_round_date = Round.objects.get_previous_round().date
            next_round_date = Round.objects.get_next_round().date
        except Exception, e:
            self.stdout.write('Warning: Couldn\'t find previous or next round date.')

        participating_schools = set()
        for season_name in current_seasons:
            participating_schools = (participating_schools | set(m.school for m in Membership.objects.filter(season__name=season_name)))

        if options['all']:
            recipients = (
                [school.contact_email for school in School.objects.all()] +
                [player.user.email 
                    for player in Player.objects.all()
                    if (player.user and player.receiveSpam)]
            )
        else:
            recipients = (
                [school.contact_email for school in participating_schools] +
                [player.user.email 
                    for school in participating_schools
                    for player in school.player_set.all()
                    if (player.user and player.receiveSpam)]
            )


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
