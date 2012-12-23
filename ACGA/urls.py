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
)

# Event pages - need to be updated manually.
# Main upcoming event is displayed on /events
# Archived events are given their own pages
# Remember to update event_template.html to update listing of all past events
urlpatterns += patterns('CGA.ACGA.views',    
    (r'^events/$', direct_to_template, {'template': 'spring_expo_2013.html'}),
    (r'^events/spring_open_2012/$', direct_to_template, {'template': 'spring_open_2012.html'}),
    (r'^events/spring_expo_2013/$', direct_to_template, {'template': 'spring_expo_2013.html'}),

)
