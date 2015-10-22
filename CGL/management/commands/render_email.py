import itertools
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
        choice = raw_input("Select a template:\n1. intro_email\n2. weekly_email\n3. bug_captains")
        if choice == "1":
            school_name = raw_input("Which school?")
            self.render_introductory_email(school_name)
        elif choice == "2":
            self.render_weekly_email()
        elif choice == "3":
            self.render_captain_bugging_email()


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

        recipients = itertools.chain(school.all_contact_emails() for school in participating_schools)

        c = Context(locals())
        self.stdout.write(t.render(c))

    def render_captain_bugging_email(self):
        with open(os.path.join(template_dir, "bug_captains.txt")) as f:
            t = template.Template(f.read())

        previous_round = Round.objects.get_previous_round()
        guilty_schools = []
        for match in previous_round.match_set.all():
            if any(game.team1_player.name.startswith("Unknown") for game in match.game_set.all()):
                guilty_schools.append(match.team1.school)
            if any(game.team2_player.name.startswith("Unknown") for game in match.game_set.all()):
                guilty_schools.append(match.team2.school)

        recipients = itertools.chain(*(school.all_contact_emails() for school in guilty_schools))

        c = Context(locals())
        self.stdout.write(t.render(c))
