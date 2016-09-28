from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy

from CGL.captain_views import edit_all_matches, edit_season_matches, edit_match, update_players, edit_school, edit_player, create_player

from CGL.admin_views import admin_dashboard, email_dashboard, render_introductory_email_view, round_pairings, update_scores

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
    url(r'^matches/$', RedirectView.as_view(url=reverse_lazy('edit_all_matches'))),
    url(r'^seasons/current/matches/$', edit_all_matches, name="edit_all_matches"),
    url(r'^seasons/([A-Za-z0-9_-]{1,50})/matches/$', edit_season_matches, name="edit_season_matches"),
    url(r'^matches/([0-9]{1,4})/edit$', edit_match, name="edit_match"),
    url(r'^games/([0-9]{1,4})/update_players/$', update_players, name="update_players"),
    url(r'^schools/([A-Za-z0-9_-]{1,50})/edit$', edit_school, name="edit_school"),
    url(r'^players/new$', create_player, name="create_player"),
    url(r'^players/([0-9]{1,4})/edit$', edit_player, name="edit_player"),
)

urlpatterns += patterns("",
    url(r'^admin/$', admin_dashboard, name="admin_dashboard"),
    url(r'^admin/commands/round_pairings/$', round_pairings, name="admin_round_pairings"),
    url(r'^admin/commands/update_scores/$', update_scores, name="admin_update_scores"),
    url(r'^admin/emails/$', email_dashboard, name="email_dashboard"),
    url(r'^admin/emails/intro_email/([0-9]{1,4})/$', render_introductory_email_view),
)