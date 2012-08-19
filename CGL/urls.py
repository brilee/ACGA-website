from django.conf.urls.defaults import *

urlpatterns = patterns('CGA.CGL.views',
    (r'^$', 'display_CGL'
    ),
    (r'^results/$', 'display_results'
    ),
    (r'^results/([A-Za-z_-]{1,50})/$', 'display_season'
    ),
    (r'^games/([0-9]{1,4})/$', 'display_game'
    ),

    )
