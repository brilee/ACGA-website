from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('CGA.CGL.views',
    (r'^$', direct_to_template, {'template': 'CGL.html'}),
    (r'^schools/$', 'display_school'),
    (r'^schools/([A-Za-z_-]{1,50})/$', 'display_roster'),                       
    (r'^results/$', 'display_results'),
    (r'^results/([A-Za-z_-]{1,50})/$', 'display_season'),
    (r'^players/$', 'display_player_search'),
    (r'^players/([A-Za-z_-]{1,50})/$', 'display_player'),
    (r'^games/([0-9]{1,4})/$', 'display_game'),
    (r'^join/$', redirect_to, {'url': '/contact/'}),
)
