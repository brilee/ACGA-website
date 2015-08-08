# You must include a reference to these context processors in settings.py,
# under "TEMPLATE_CONTEXT_PROCESSORS".


from models import Season
from settings import current_seasons

from ogs.client import get_ladder_top_players


def sidebar_CGL(request):
    top_players = get_ladder_top_players(1926)

    return {
        'current_seasons': [Season.objects.get(name=s) for s in current_seasons],
        'iCGL_top_players': top_players,
    }
