from django.conf.urls.defaults import *
from django.views import static
from django.views.generic.simple import direct_to_template

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
    (r'^home/$', direct_to_template, {
	'template': 'home.html', 'extra_context': {'NavID': 'home', 'sidebar': 'sidebar.html'},
	}),
    (r'^links/$', direct_to_template, {
	'template': 'links.html', 'extra_context': {'NavID': 'links', 'sidebar': 'sidebar.html'},
	}),
    (r'^ing/$', direct_to_template, {
	'template': 'ing.html', 'extra_context': {'NavID': 'ing', 'sidebar': 'sidebar.html'},
	}),
    (r'^about/$', direct_to_template, {
	'template': 'about.html', 'extra_context': {'NavID': 'about', 'sidebar': 'sidebar3.html'},
	}),
    (r'^style.css/$', direct_to_template, {
	'template': 'style.css'
	}),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/cole/Webs/CGA/site_media'}),
)

urlpatterns += patterns('CGA.membership.views',
    (r'^membership/$', direct_to_template, {
	'template': 'membership.html', 'extra_context': {'NavID': 'membership', 'sidebar': 'sidebar2.html'}
	}),
    (r'^membership/login/$', 'login_user'),
    (r'^membership/profile/$', 'profile'),

)

urlpatterns += patterns('CGA.contact.views',
    (r'^contact/$', 'contact'),
    (r'^contact/thanks/$', direct_to_template, {
        'template': 'thanks.html', 'extra_context': {'NavID': 'contact', 'sidebar': 'sidebar2.html'},
	}),
)

urlpatterns += patterns('CGA.whatsnew.views',
    (r'^whatsnew/$', 'whatsnew'),
)

urlpatterns += patterns('CGA.images.views',
    (r'^images/$', 'images'),
)
