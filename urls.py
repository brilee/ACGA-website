from django.conf.urls.defaults import *
from django.views import static
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('CGA.views',
    # Example:
    #(r'^login/$', 'auth.views.login_user'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', direct_to_template, {
        'template': 'home.html' }
    ),
    (r'^home/$', direct_to_template, {
	'template': 'home.html'	}
    ),
    (r'^links/$', direct_to_template, {
	'template': 'links.html'}
    ),
    (r'^ing/$', direct_to_template, {
	'template': 'ing.html'}
    ),
    (r'^about/$', direct_to_template, {
	'template': 'about.html'}
    ),
    (r'^tournaments/$', direct_to_template, {
	'template': 'tournaments.html'}
    ),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/var/www/CGA/site_media'}),
)

urlpatterns += patterns('CGA.contact.views',
    (r'^contact/$', 'contact'),
    (r'^contact/thanks/$', direct_to_template, {
        'template': 'thanks.html'}),
)
