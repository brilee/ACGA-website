from django.conf.urls import *
from django.views import static
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from django.conf import settings
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin pages
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Static content
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ADMIN_MEDIA_ROOT}),
)

urlpatterns += patterns('contact.views',
    # Contact page
    (r'^contact/$', 'contact'),
    (r'^contact/thanks/$', TemplateView.as_view(template_name='thanks.html')),
    (r'^CGL/join/$', 'join_CGL'),
    (r'^CGL/join/thanks/$', TemplateView.as_view(template_name='thanks_CGL.html')),
)

urlpatterns += patterns('',
    # Account registration/login
    (r'^accounts/', include('accounts.urls')),
    #(r'^accounts/', include('registration.backends.default.urls')),
    # CGL subportal
    (r'^CGL/', include('CGL.urls')),

    # ACGA main pages
    # This must come last, since the regex matches everything.
    (r'', include('ACGA.urls')),
)

