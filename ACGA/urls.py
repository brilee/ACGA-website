from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('CGA.ACGA.views',    
    (r'^$', 'display_home'),
    (r'^home/$', 'display_home'),
    (r'^links/$', direct_to_template, {'template': 'links.html'}),
    (r'^ing/$', direct_to_template, {'template': 'ing.html'}),
    (r'^about/$', direct_to_template, {'template': 'about.html'}),
    (r'^members/$', 'display_members'),
    (r'^news/$', 'display_news'),
    (r'^news/([0-9]{1,4})/$', 'display_post'),
    (r'^allemail/$', 'display_emails'),                       
)
