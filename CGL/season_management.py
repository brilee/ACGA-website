from CGL.models import Team, School

def get_actively_participating_schools(current_season_names):
    school_ids = [d['school'] for d in Team.objects.filter(season__name__in=current_season_names).values("school")]

    return School.objects.filter(id__in=school_ids)
