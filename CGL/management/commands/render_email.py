from django.core.management.base import BaseCommand, CommandError
from django.template import Context, loader

from CGL.models import Round
from CGL.settings import current_seasons as current_season_names
from CGL.season_management import get_actively_participating_schools

class Command(BaseCommand):
    args = ''
    help = '''Renders an email to rendered_email.txt containing a formatted email to be sent out.'''

    def handle(self, *args, **options):
        try:
            previous_round_date = Round.objects.get_previous_round().date
            next_round_date = Round.objects.get_next_round().date
        except Exception as e:
            self.stdout.write('Warning: Couldn\'t find previous or next round date.')

        participating_schools = get_actively_participating_schools(current_season_names)

        recipients = (
            [school.contact_email for school in participating_schools] +
            [player.user.email 
                for school in participating_schools
                for player in school.player_set.all()
                if (player.user and player.receiveSpam)]
        )


        c = Context(locals())
        
        try:
            email_template = 'weekly_email'
            t = loader.get_template(email_template)
        except Exception as e:
            self.stdout.write(str(e))
            raise CommandError('Email template not found')

        with open('templates/rendered-email', 'w') as f:
            f.write(t.render(c))

        self.stdout.write('Email rendered to templates/rendered-email.\n')
