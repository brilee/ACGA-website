import urlparse
from django.core.urlresolvers import reverse

from captain_auth import AUTH_KEY_COOKIE_NAME
from CGL.models import CurrentSeasons, Team, School, SchoolAuth
from django.conf import settings

def get_actively_participating_schools():
    school_ids = [d['school'] for d in Team.objects.filter(season__in=CurrentSeasons.objects.get()).values("school")]

    return School.objects.filter(id__in=school_ids)

def regenerate_school_auth_keys(school):
    SchoolAuth.objects.filter(school=school).delete()
    auth, created = SchoolAuth.objects.get_or_create(school=school)
    return (school.contact_email,
        urlparse.urlunparse([
            "",
            settings.WEB_URL,
            reverse("captain_dashboard"), "",
            AUTH_KEY_COOKIE_NAME + "=" + auth.secret_key, ""]
    ))
