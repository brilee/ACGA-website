import urlparse
from django.core.urlresolvers import reverse

from captain_auth import AUTH_KEY_COOKIE_NAME
from CGL.models import Team, School, SchoolAuth
from django.conf import settings

def get_actively_participating_schools(current_season_names):
    school_ids = [d['school'] for d in Team.objects.filter(season__name__in=current_season_names).values("school")]

    return School.objects.filter(id__in=school_ids)

def regenerate_school_auth_keys(school):
    SchoolAuth.objects.filter(school=school).delete()
    auth, created = SchoolAuth.objects.get_or_create(school=school)
    return (school.contact_email,
        urlparse.urlunparse([
            "",
            settings.WEB_URL,
            reverse("display_all_matches"), "",
            AUTH_KEY_COOKIE_NAME + "=" + auth.secret_key, ""]
    ))
