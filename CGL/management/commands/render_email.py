import os

from django.core.management.base import BaseCommand
from django.template import Context
from django import template

from CGL.models import Round, Season, School, SchoolAuth
from CGL.settings import current_seasons as current_season_names
from CGL.season_management import get_actively_participating_schools

template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "email_templates")

class Command(BaseCommand):
    args = ''
    help = '''Renders an email to rendered_email.txt containing a formatted email to be sent out.'''

    def handle(self, *args, **options):
        choice = raw_input("Select a template:\n1. intro_email\n2. weekly_email")
        if choice == "1":
            school_name = raw_input("Which school?")
            self.render_introductory_email(school_name)
        elif choice == "2":
            self.render_weekly_email()


    def render_introductory_email(self, school_name):
        with open(os.path.join(template_dir, "intro_email.txt")) as f:
            t = template.Template(f.read())

        school = School.objects.get(name__contains=school_name)
        school_auth = SchoolAuth.objects.get(school=school)

        from CGL.captain_auth import AUTH_KEY_COOKIE_NAME
        context = Context(locals())
        self.stdout.write(t.render(context))


    def render_weekly_email(self):
        with open(os.path.join(template_dir, "weekly_email.txt")) as f:
            t = template.Template(f.read())

        try:
            previous_round_date = Round.objects.get_previous_round().date
            next_round_date = Round.objects.get_next_round().date
        except Exception as e:
            self.stderr.write('Warning: Couldn\'t find previous or next round date.')

        current_seasons = [Season.objects.get(name=s) for s in current_season_names]
        participating_schools = get_actively_participating_schools(current_season_names)

        recipients = (
            [school.contact_email for school in participating_schools] +
            [player.user.email 
                for school in participating_schools
                for player in school.player_set.all()
                if (player.user and player.receiveSpam)]
        )


        c = Context(locals())
        self.stdout.write(t.render(c))
