from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from CGL.captain_views import display_all_matches, display_match, update_players

urlpatterns = patterns('CGL.views',
    (r'^$', TemplateView.as_view(template_name='CGL.html')),
    (r'^rules/$', TemplateView.as_view(template_name='CGL_rules.html')),
    (r'^schools/$', 'display_schools'),
    (r'^schools/([A-Za-z0-9_-]{1,50})/$', 'display_roster'),
    (r'^results/$', 'display_current_seasons'),
    (r'^results/([A-Za-z0-9_-]{1,50})/$', 'display_seasons'),
    (r'^players/$', 'display_player_search'),
    (r'^players/([0-9]{1,4})/$', 'display_player'),
    (r'^games/([0-9]{1,4})/$', 'display_game'),
    (r'^games/([0-9]{1,4})/submit/$', 'submit_comment'),
)

urlpatterns += patterns("",
    url(r'^matches/$', display_all_matches, name="display_all_matches"),
    url(r'^matches/([0-9]{1,4})/$', display_match, name="display_match"),
    url(r'^games/([0-9]{1,4})/update_players/$', update_players, name="update_players")
)
