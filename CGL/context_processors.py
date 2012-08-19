# You must include a reference to these context processors in settings.py,
# under "TEMPLATE_CONTEXT_PROCESSORS".


from models import Round, Season
from CGA.ACGA.models import Newsfeed
from settings import current_season_name

def current_season(request):
    current_season = Season.get(name=current_season_name)
    return {'current_season': current_season}

def sidebar_CGL(request):
    sidebar_upcoming_round = Round.objects.get_next_round()
    sidebar_recent_rounds = Round.objects.get_recent_rounds(2)
    return {'sidebar_upcoming_round': sidebar_upcoming_round,
            'sidebar_recent_rounds': sidebar_recent_rounds,}

