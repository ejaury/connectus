from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^connectus/', include('connectus.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', 'connectus.main.views.index'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name':'main/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name':'main/index.html'}),
    (r'^courses/', include('connectus.courses.urls')),
    (r'^grades/', include('connectus.grades.urls')),
    (r'^schedule/', include('connectus.schedule.urls')),
    (r'^admin/', include(admin.site.urls)),
    # TODO: this conf is for production only
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {
      'document_root': '/home/edwin/connectus/media/', 'show_indexes': True
    }),
)
