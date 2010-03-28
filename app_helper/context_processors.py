from django.core.urlresolvers import reverse
from connectus.app_helper.helper import NavigationTree
from connectus.courses.models import Course, CourseRegistration

def sidebar(request):
  # TODO: order by course title
  if request.user.is_anonymous():
    return {}

  user_groups = request.user.groups.all()
  if user_groups:
    menus = NavigationTree.get_main_navi(user_groups)
  else:
    return {} 
  
  #TODO need a better way to check for groups
  if user_groups[0].name == 'Teacher': 
    #TODO: check which class this teacher belongs to 
    courses = Course.objects.all()
  elif user_groups[0].name == 'Student':
    regs = CourseRegistration.objects.filter(student=request.user)
    course_ids = []
    for reg in regs:
      course_ids.append(reg.course.id)
    courses = Course.objects.filter(id__in=course_ids)
  else:
    courses = []

  return {
    'courses': courses,
    'menus': menus
  }
