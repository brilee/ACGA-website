from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('CGA.CGL.views',
    (r'^$', direct_to_template, {'template': 'CGL.html'}),
    (r'^results/$', 'display_results'),
    (r'^results/([A-Za-z_-]{1,50})/$', 'display_season'),
    (r'^games/([0-9]{1,4})/$', 'display_game'),
)
