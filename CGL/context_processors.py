# You must include a reference to these context processors in settings.py,
# under "TEMPLATE_CONTEXT_PROCESSORS".


from models import Round, Season, Bye
from ACGA.models import Newsfeed
from settings import current_season_nameA, current_season_nameB


def sidebar_CGL(request):
    def get_bye(**kwargs):
        try:
            return Bye.objects.filter(**kwargs)
        except:
            return []
    
    current_seasonA = Season.objects.get(name=current_season_nameA)
    current_seasonB = Season.objects.get(name=current_season_nameB)
    
    sidebar_upcoming_roundA = Round.objects.get_next_round(season=current_seasonA)
    sidebar_upcoming_roundB = Round.objects.get_next_round(season=current_seasonB)
    sidebar_recent_roundA = Round.objects.get_previous_round(season=current_seasonA)
    sidebar_recent_roundB = Round.objects.get_previous_round(season=current_seasonB)
    
    sidebar_byesA = get_bye(round=sidebar_upcoming_roundA)
    sidebar_byesB = get_bye(round=sidebar_upcoming_roundB)
    sidebar_recent_byesA = get_bye(round=sidebar_recent_roundA)
    sidebar_recent_byesB = get_bye(round=sidebar_recent_roundB)

    return locals()

