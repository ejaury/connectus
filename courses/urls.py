from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^connectus/', include('connectus.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', 'connectus.courses.views.index'),
    (r'^(?P<course_id>\d+)/attendance/$', 'connectus.courses.views.attendance'),
    (r'^(?P<course_id>\d+)/grades/$', 'connectus.courses.views.grades'),
    (r'^(?P<course_id>\d+)/grades/update$', 'connectus.courses.views.update_grades'),
    (r'^(?P<course_id>\d+)/view_seating_plan/$', 'connectus.courses.views.view_seating_plan'),
    (r'^(?P<course_id>\d+)/update_seating_order$',
      'connectus.courses.views.update_seating_order'),
    # (r'^admin/', include(admin.site.urls)),
)
