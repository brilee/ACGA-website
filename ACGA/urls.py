from django.conf.urls import *
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = patterns('ACGA.views',    
    (r'^$', TemplateView.as_view(template_name='home.html')),
    (r'^home/$', TemplateView.as_view(template_name='home.html')),
    (r'^resources/$', 'display_resources'),
    (r'^ing/$', TemplateView.as_view(template_name='ing.html')),
    (r'^about/$', TemplateView.as_view(template_name='about.html')),
    (r'^members/$', 'display_members'),
    (r'^allemail/$', 'display_emails'),
    (r'^events/$', 'display_upcoming_event'),
    (r'^events/([A-Za-z0-9_-]{1,50})/$', 'display_event'),
)
