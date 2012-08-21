from django.core.management.base import BaseCommand, CommandError
from CGA.CGL.models import Season


class Command(BaseCommand):
    args = '<Season Name>'
    help = '''Changes current season. This will cause the website's default
            behavior to update (sidebars, /cgl/results, etc.)'''

    def handle(self, *args, **options):
        if not args:
            raise CommandError('Must specify a season!')
        try:
            season = Season.objects.get(name=args[0])
        except:
            raise CommandError('Season not found. (Try creating the season first). Name must be exact, case-insensitive.')

        f = open('CGL/settings.py', 'w')
        f.write("current_season_name = '%s'" % season.name)
        f.close()

        self.stdout.write('Current season updated to %s\n' % season.name)
        self.stdout.write('Remember to restart the server (>>>apachectl restart) to see effects\n')
