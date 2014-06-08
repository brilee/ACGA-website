from django.conf.urls import *
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = patterns('CGL.views',
    (r'^$', TemplateView.as_view(template_name='CGL.html')),
    (r'^rules/$', TemplateView.as_view(template_name='CGL_rules.html')),
    (r'^schools/$', 'display_school'),
    (r'^schools/([A-Za-z_-]{1,50})/$', 'display_roster'),                       
    (r'^results/$', 'display_current_seasons'),
    (r'^results/([A-Za-z_-]{1,50})/$', 'display_seasons'),
    (r'^players/$', 'display_player_search'),
    (r'^players/([0-9]{1,4})/$', 'display_player'),
    (r'^games/([0-9]{1,4})/$', 'display_game'),
    (r'^games/([0-9]{1,4})/submit/$', 'submit_comment'),
)
