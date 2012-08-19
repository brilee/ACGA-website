# You must include a reference to these context processors in settings.py,
# under "TEMPLATE_CONTEXT_PROCESSORS".

from models import Newsfeed

def sidebar_ACGA(request):
    sidebar_latest_news = Newsfeed.objects.order_by('-pub_date')[:3]
    return {'sidebar_latest_news': sidebar_latest_news,}

