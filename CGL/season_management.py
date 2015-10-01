from CGL.models import Team, Season

def get_actively_participating_schools(current_season_names):
    current_seasons = Season.objects.filter(name__in=current_season_names)
    participating_schools = set()
    for season in current_seasons:
        participating_schools = (participating_schools | set(m.school for m in Team.objects.filter(season=season)))

    return participating_schools
