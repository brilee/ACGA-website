import os, socket, random, string, datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core import management
from django.contrib.auth.models import User
import settings
from CGL.models import *
from accounts.models import *
from ACGA.models import *
from CGL.settings import current_seasons

def randomstr():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10)).capitalize()

class Command(BaseCommand):
    args = 'none'
    help = '''Initializes a database for cgl website (Nukes and recreates database on each execution)'''

    def handle(self, *args, **options):
        # basic sanity check to make sure we're not nuking the production database if we accidentally run this command on the server.
        # you'll have to manually add your socket.gethostname() entry to this line to successfully nuke and run this command.
        if (settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'
            and settings.DEBUG == True
            and settings.WEB_URL == '127.0.0.1:8000/'
            and socket.gethostname() == 'Brians-MacBook-Air.local'):

            self.stdout.write('deleting existing database\n')
            try:
                os.remove(settings.DATABASES['default']['NAME'])
                self.stdout.write('deleted database\n')
            except:
                self.stdout.write('couldn\'t delete database\n')
                pass
        else:
            raise CommandError("You don't seem to be developing locally! Quitting to be safe.")

        # setup the basic empty tables
        management.call_command('syncdb', interactive=False)
        management.call_command('migrate', 'CGL', interactive=False)
        management.call_command('migrate', 'ACGA', interactive=False)
        management.call_command('migrate', 'accounts', interactive=False)
        self.stdout.write('database tables recreated\n')

        u = User(username='admin')
        u.set_password('password')
        u.is_superuser = True
        u.is_staff = True
        u.save()
        self.stdout.write('superuser created with username/password : admin/password\n')

        brilee = User(username='brilee')
        brilee.set_password('password')
        brilee.save()
        self.stdout.write('basic user created with username/password : brilee/password\n')
        self.stdout.write('this account also gets edit permissions for all schools\n')

        schoolnames = ('Testing University',
                       'Testing College',
                       'Underwater Basket Weaving College',
                       'Kitty University')
        schools = [School(name=n) for n in schoolnames]
        for s in schools:
            s.save()

        for s in schools:
            for i in range(3):
                p = Player(name=randomstr(), school=s)
                p.save()

        # This is so that context processors load correctly.
        real_seasons = [Season(name=s) for s in current_seasons]
        for s in real_seasons:
            s.save()

        fake_seasons = [Season(name='test ' + s) for s in current_seasons]

        for s in fake_seasons:
            s.save()

        for s in fake_seasons:
            for school in schools:
                membership = Membership(school=school, season=s)
                membership.save()
            for datedelta in (datetime.timedelta(days=-30),
                              datetime.timedelta(days=-7),
                              datetime.timedelta(days=1),
                              datetime.timedelta(days=10),
                              datetime.timedelta(days=30),
                              datetime.timedelta(days=100),):
                r = Round(season=s, date=datetime.datetime.today()-datedelta)
                r.save()
                for i in range(2):
                    m = Match(school1=random.choice(schools), school2=random.choice(schools), round=r)
                    m.save()
                    if m.round.date < datetime.datetime.today():
                        for i in range(3):
                            g = Game(
                                white_player=random.choice(m.school1.player_set.all()),
                                black_player=random.choice(m.school2.player_set.all()),
                                match=m,
                                board=i+1,
                                white_school='School1',
                                winning_school='School2',
                                gamefile=File(open('site_media/test_file'))
                                )
                            g.save()

        self.stdout.write('Updating school rankings and records\n')
        for s in fake_seasons:
            management.call_command('update_scores', s.name, interactive=False)

        self.stdout.write('Test database entries created\n')
