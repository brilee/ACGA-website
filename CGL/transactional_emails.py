import os
import itertools

from django.template import Context
from django import template

from CGL.models import Round, Season, School, SchoolAuth
from CGL.settings import current_seasons as current_season_names
from CGL.season_management import get_actively_participating_schools

template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "email_templates")

def get_all_email_addresses():
    participating_schools = get_actively_participating_schools(current_season_names)

    return itertools.chain(*(school.all_contact_emails() for school in participating_schools))

def render_introductory_email(school_name):
    with open(os.path.join(template_dir, "intro_email.txt")) as f:
        t = template.Template(f.read())

    school = School.objects.get(name__contains=school_name)
    school_auth = SchoolAuth.objects.get(school=school)

    from CGL.captain_auth import AUTH_KEY_COOKIE_NAME
    context = Context(locals())
    return t.render(context)


def render_weekly_email():
    with open(os.path.join(template_dir, "weekly_email.txt")) as f:
        t = template.Template(f.read())

    previous_round = Round.objects.get_previous_round()
    next_round = Round.objects.get_next_round()

    current_seasons = [Season.objects.get(name=s) for s in current_season_names]

    c = Context(locals())
    return t.render(c)

def render_reminder_email():
    with open(os.path.join(template_dir, "bug_captains.txt")) as f:
        t = template.Template(f.read())

    previous_round = Round.objects.get_previous_round()
    guilty_schools = set()
    for match in previous_round.match_set.all():
        if any(game.team1_player.name.startswith("Unknown") for game in match.game_set.all()):
            guilty_schools.add(match.team1.school)
        if any(game.team2_player.name.startswith("Unknown") for game in match.game_set.all()):
            guilty_schools.add(match.team2.school)

    c = Context(locals())
    return t.render(c)
