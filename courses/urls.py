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
    (r'^(?P<course_id>\d+)/$', 'connectus.courses.views.detail'),
    (r'^(?P<course_id>\d+)/grades/$', 'connectus.courses.views.grades'),
    (r'^(?P<course_id>\d+)/grades/update$', 'connectus.courses.views.update_grades'),
    (r'^(?P<course_id>\d+)/view_seating_plan/$', 'connectus.courses.views.view_seating_plan'),
    (r'^(?P<course_id>\d+)/view_own_grades/$',
      'connectus.courses.views.view_own_grades'),
    (r'^(?P<course_id>\d+)/update_seating_order$',
      'connectus.courses.views.update_seating_order'),

    #
    # Attendance
    #
    (r'^(?P<course_id>\d+)/attendance/$', 'connectus.courses.views.attendance'),
    (r'^(?P<course_id>\d+)/attendance/update$',
      'connectus.courses.views.update_attendance'),

    #
    # File uploads/Assignment submissions
    #
    (r'^(?P<course_id>\d+)/gradeables/uploaded/$',
      'connectus.submissions.views.view_uploaded'),
    (r'^(?P<course_id>\d+)/gradeables/uploaded/edit/$',
      'connectus.submissions.views.update_uploaded'),
    (r'^(?P<course_id>\d+)/submissions/$',
      'connectus.submissions.views.view_submissions'),
    # (r'^admin/', include(admin.site.urls)),
)
