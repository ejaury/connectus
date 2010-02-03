from django.core.urlresolvers import reverse
from connectus.courses.models import Course

def sidebar(request):
  # TODO: order by course title
  courses = Course.objects.all()
  return { 'courses': courses } 
