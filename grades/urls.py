from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^connectus/', include('connectus.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', 'connectus.grades.views.index'),
    #(r'^add/$', 'connectus.grades.views.add'),
    (r'^(?P<course_id>\d+)/add/$', 'connectus.grades.views.add'),
    (r'^(?P<grade_id>\d+)/edit/$', 'connectus.grades.views.edit'),
    (r'^(?P<grade_id>\d+)/delete/$', 'connectus.grades.views.delete'),
    (r'^(?P<grade_id>\d+)/$', 'connectus.grades.views.detail'),
    (r'^courses/(?P<course_id>\d+)/$', 'connectus.grades.views.list_by_course'),
    #(r'^admin/', include(admin.site.urls)),
)
