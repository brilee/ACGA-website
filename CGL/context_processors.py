# You must include a reference to these context processors in settings.py,
# under "TEMPLATE_CONTEXT_PROCESSORS".


from models import Round, Season
from CGA.ACGA.models import Newsfeed
from settings import current_season_nameA, current_season_nameB


def current_season(request):
    current_seasonA = Season.get(name=current_season_nameA)
    current_seasonB = Season.get(name=current_season_nameB)
    return locals()

def sidebar_CGL(request):
    sidebar_upcoming_roundA = Round.objects.get_next_round(current_season_nameA)
    sidebar_upcoming_roundB = Round.objects.get_next_round(current_season_nameB)
    sidebar_recent_roundA = Round.objects.get_recent_rounds(current_season_nameA, 1)
    sidebar_recent_roundB = Round.objects.get_recent_rounds(current_season_nameB, 1)
    return locals()

