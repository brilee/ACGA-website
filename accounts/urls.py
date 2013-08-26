from django.conf.urls.defaults import *
from django.views import static
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout
from django.conf import settings

urlpatterns = patterns('accounts.urls',
    # User homepage / select a player to link to
    (r'^profile/$', 'CGL.views.redirect_to_player_profile'),
    # Account registration/login
    (r'', include('registration.backends.default.urls')),
    #(r'^$', direct_to_template, {'template': 'CGL.html'}),
)

