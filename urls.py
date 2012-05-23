from django.conf.urls.defaults import *
from django.views import static
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('CGA.CGL.views',
    # Example:
    #(r'^login/$', 'auth.views.login_user'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'display_home'
    ),
    (r'^home/$', 'display_home'
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
    (r'^CGL/$', 'display_CGL'
    ),
    (r'^CGL/results/$', 'display_results'
    ),
    (r'^CGL/results/([A-Za-z_-]{1,50})/$', 'display_season'
    ),
    (r'^CGL/games/([0-9]{1,4})/$', 'display_game'
    ),
    (r'^members/$', 'display_members'
    ),
    (r'^members/([A-Za-z_-]{1,50})/$', 'display_school'
    ),                       
    (r'^news/$', 'display_news'
    ),
    (r'^news/([0-9]{1,4})/$', 'display_post'
    ),
    (r'^allemail/$', 'display_emails'
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
