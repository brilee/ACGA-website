from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('CGA.ACGA.views',    
    (r'^$', 'display_home'),
    (r'^home/$', 'display_home'),
    (r'^resources/$', 'display_resources'),
    (r'^ing/$', direct_to_template, {'template': 'ing.html'}),
    (r'^about/$', direct_to_template, {'template': 'about.html'}),
    (r'^members/$', 'display_members'),
    (r'^allemail/$', 'display_emails'),
    (r'^events/$', 'display_upcoming_event'),
    (r'^events/([A-Za-z0-9_-]{1,50})/$', 'display_event'),
)
