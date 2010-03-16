import xml.etree.ElementTree
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from connectus.courses.models import CourseRegistration
from connectus.schedule.models import CourseCalendar

CAL_BASE_HTML = "<iframe src=\"http://www.google.com/calendar/embed?title= &amp;height=600&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;ctz=America%2FVancouver\" style=\" border-width:0 \" width=\"720\" height=\"600\" frameborder=\"0\" scrolling=\"no\"></iframe>"

@login_required(redirect_field_name='next')
def view(req):
  # get calendar titles for classes that this student is registered in
  #   if a teacher, display everything
  student_group = Group.objects.get(name='Student')
  if student_group not in req.user.groups.all():
    course_calendars = CourseCalendar.objects.all()
  else:
    registrations = CourseRegistration.objects.filter(student=req.user)
    registered_courses = []
    for reg in registrations:
      registered_courses.append(reg.course)
    course_calendars = CourseCalendar.objects.filter(course__in=registered_courses)

  # get calendar ids and colors
  get_params = []
  for cal in course_calendars:
    get_params.append(__generate_get_params(cal.calendar_id, cal.calendar_color))
    
  # generate embeddable HTML for calendar
  html = __gen_embeddable_html(get_params)
  return render_to_response('schedule/view.html',
                            { 'cal_html': html },
                            context_instance=RequestContext(req))

def __generate_get_params(cal_id, cal_color):
  return ('&src=%s&color=%%23%s') % (cal_id, cal_color)

def __gen_embeddable_html(get_params):
  elem = xml.etree.ElementTree.fromstring(CAL_BASE_HTML)
  src_attr = elem.get('src')
  elem.set('src', src_attr + ''.join(get_params))
  # HACK: otherwise, iframe element would not be enclosed properly
  elem.text = ' '
  return xml.etree.ElementTree.tostring(elem)
