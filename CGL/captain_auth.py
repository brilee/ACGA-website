from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from CGL.models import SchoolAuth, Player, School, Match, Forfeit, Game

AUTH_KEY_COOKIE_NAME = "captain_school_auth"

def get_secret_key(request):
    # can auth either first time with a queryparam or with cookie
    if AUTH_KEY_COOKIE_NAME in request.GET:
        secret_key = request.GET.get(AUTH_KEY_COOKIE_NAME)
    elif request.COOKIES.has_key(AUTH_KEY_COOKIE_NAME):
        secret_key = request.COOKIES[AUTH_KEY_COOKIE_NAME]
    else:
        return None
    if SchoolAuth.objects.filter(secret_key=secret_key).count() == 0:
        return None

    return secret_key

def set_secret_key(response, secret_key):
    response.set_cookie(AUTH_KEY_COOKIE_NAME, secret_key, max_age=52*7*24*60*60)

def get_school(request):
    secret_key = get_secret_key(request)
    auth = SchoolAuth.objects.get(secret_key=secret_key)
    return auth.school

def school_auth_required(view):
    def wrapped(request, *args, **kwargs):
        secret_key = get_secret_key(request)
        if secret_key is None:
            return HttpResponseForbidden()

        response = view(request, *args, **kwargs)
        set_secret_key(response, secret_key)
        return response
    return wrapped

def check_auth(school, obj):
    if type(obj) == Player:
        return obj.school == school
    elif type(obj) == School:
        return obj == school
    elif type(obj) == Match:
        return obj.team1.school == school or obj.team2.school == school
    elif type(obj) == Game:
        return obj.match.team1.school == school or obj.match.team2.school == school
    elif type(obj) == Forfeit:
        return obj.match.team1.school == school or obj.match.team2.school == school
    else:
        return False