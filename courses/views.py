from django.shortcuts import get_object_or_404, render_to_response
from connectus.courses.models import Course

def index(req):
  all_courses = Course.objects.all().order_by('-id')
  return render_to_response('courses/index.html', {'all_courses': all_courses})
