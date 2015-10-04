from django.conf.urls import *
from django.shortcuts import redirect
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
        {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ADMIN_MEDIA_ROOT}),
    # CGL subportal
    (r'^CGL/', include('CGL.urls')),
)

# Redirects to the ACGA portal that was redone on Hubspot
def my_redirect(to_url):
    def redirector(request):
        return redirect(to_url)
    return redirector

urlpatterns += patterns('',   
    (r'^$', my_redirect('http://www.college-go.org')),
    (r'^home/$', my_redirect('http://www.college-go.org')),
    (r'^resources/$', my_redirect('http://www.college-go.org/resources')),
    (r'^ing/$', my_redirect('http://www.college-go.org/ing-foundation')),
    (r'^about/$', my_redirect('http://www.college-go.org/about-us')),
    (r'^contact/?$', my_redirect('http://www.college-go.org/contact-us')),
    (r'^members/?$', my_redirect('/CGL/schools/')),
    (r'^events/$', my_redirect('http://www.college-go.org/events')),
    (r'^/events/spring_open_2012/$', my_redirect('http://www.college-go.org/events/2012-acga-spring-go-open')),
    (r'^/events/spring_expo_2013/$', my_redirect('http://www.college-go.org/events/2012-acga-spring-go-open')),
    (r'^/events/2013_international_college_go_tournament/$', my_redirect('http://www.college-go.org/events/2013-international-collegiate-go-tournament')),
    (r'^/events/spring_expo_2014/$', my_redirect('http://www.college-go.org/events/2014-acga-spring-go-expo')),
    (r'^/events/2014_intl_college_tournament/$', my_redirect('http://www.college-go.org/events/2014-international-collegiate-go-tournament')),
)
