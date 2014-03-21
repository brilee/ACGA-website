# You must include a reference to these context processors in settings.py,
# under "TEMPLATE_CONTEXT_PROCESSORS".


from models import Season
from settings import current_seasons

def sidebar_CGL(request):
    return {'current_seasons': [Season.objects.get(name=s) for s in current_seasons]}
