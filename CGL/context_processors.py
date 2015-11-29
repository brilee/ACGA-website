# You must include a reference to these context processors in settings.py,
# under "TEMPLATE_CONTEXT_PROCESSORS".

from django.core.cache import cache

from models import Season
from settings import current_seasons

from ogs.client import get_ladder_top_players

def django_caching(f):
    def wrapped(*args):
        cached = cache.get(str(args))
        if cached:
            return cached
        else:
            result = f(*args)
            cache.set(str(args), result, 60*10)
            return result
    return wrapped

get_ladder_top_players = django_caching(get_ladder_top_players)


def sidebar_CGL(request):
    top_players = get_ladder_top_players(1926)

    return {
        'current_seasons': [Season.objects.get(name=s) for s in current_seasons],
        'iCGL_top_players': top_players,
    }
