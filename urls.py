from django.conf.urls.defaults import *
from django.views import static
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin pages
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Static content
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/var/www/CGA/site_media/'}),
    (r'^admin/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/var/www/CGA/media/admin/'}),
)

urlpatterns += patterns('contact.views',
    # Contact page
    (r'^contact/$', 'contact'),
    (r'^contact/thanks/$', direct_to_template, {
        'template': 'thanks.html'}),

    (r'^CGL/join/$', 'join_CGL'),
    (r'^CGL/join/thanks/$', direct_to_template, {
        'template': 'thanks_CGL.html'}),
)

urlpatterns += patterns('',
    # User homepage / select a player to link to
    (r'^accounts/profile/$', 'CGL.views.redirect_to_player_profile'),
    # Account registration/login
    (r'^accounts/', include('registration.backends.default.urls')),
    # CGL subportal
    (r'^CGL/', include('CGL.urls')),

    # ACGA main pages
    # This must come last, since the regex matches everything.
    (r'', include('ACGA.urls')),
)

