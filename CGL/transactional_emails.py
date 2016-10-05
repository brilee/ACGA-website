import os
import itertools

from django.template import Context
from django import template
from django.core.mail import send_mail

from CGL.captain_auth import AUTH_KEY_COOKIE_NAME
from CGL.models import Round, CurrentSeasons, SchoolAuth
from CGL.season_management import get_actively_participating_schools

template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "email_templates")

def get_template(name):
    with open(os.path.join(template_dir, name)) as f:
        return template.Template(f.read())

def get_all_email_addresses():
    participating_schools = get_actively_participating_schools()

    return itertools.chain(*(school.all_contact_emails() for school in participating_schools))

def send_magic_link_email(school, AUTH_KEY_COOKIE_NAME=AUTH_KEY_COOKIE_NAME): # rebind AUTH_KEY_COOKIE_NAME as local()
    t = get_template("send_magic_link.txt")
    school_auth = SchoolAuth.objects.get(school=school)
    c = Context(locals())

    subject_line = "CGL Captain's dashbord -- magic link"
    email_body = t.render(c)
    recipients = [school.contact_email] + school.secondary_contacts.split(',')

    send_mail(subject_line,
              email_body,
              'cgl.tournament.director@gmail.com',
              recipients,)

def render_introductory_email(school, AUTH_KEY_COOKIE_NAME=AUTH_KEY_COOKIE_NAME): # rebind AUTH_KEY_COOKIE_NAME as local()
    t = get_template("intro_email.txt")

    school_auth = SchoolAuth.objects.get(school=school)
    c = Context(locals())

    return t.render(c)


def render_weekly_email():
    t = get_template("weekly_email.txt")

    previous_round = Round.objects.get_previous_round()
    next_round = Round.objects.get_next_round()

    current_seasons = CurrentSeasons.objects.get()

    c = Context(locals())
    return t.render(c)

def render_reminder_email():
    t = get_template("bug_captains.txt")

    previous_round = Round.objects.get_previous_round()
    guilty_schools = set()
    if previous_round:
        for match in previous_round.match_set.all():
            if any(game.team1_player.name.startswith("Unknown") for game in match.game_set.all()):
                guilty_schools.add(match.team1.school)
            if any(game.team2_player.name.startswith("Unknown") for game in match.game_set.all()):
                guilty_schools.add(match.team2.school)

    c = Context(locals())
    return t.render(c)
