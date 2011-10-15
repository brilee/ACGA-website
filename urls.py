from django.conf.urls.defaults import *
from django.views import static

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('CGA.views',
    # Example:
    #(r'^login/$', 'auth.views.login_user'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    (r'^home/$', 'home'),
    (r'^/$', 'home'),
    (r'^whatsnew/$', 'whatsnew'),
    (r'^membership/$', 'membership'),
    (r'^images/$', 'images'),
    (r'^links/$', 'links'),
    (r'^about/$', 'about'),
    (r'^ing/$', 'ing'),
    (r'^contact/$', 'contact'),
    (r'^style.css/$', 'stylesheet'),
)
#urlpatterns += patterns('',
#	
#	 (r'^style.css/$', 'stylesheet'),
# 
#)
