from django.shortcuts import get_object_or_404, render_to_response
from connectus.courses.models import Course

def index(req):
  all_courses = Course.objects.all().order_by('-id')
  return render_to_response('courses/index.html', { 'all_courses': all_courses})

def grades(req, course_id):
  course = Course.objects.get(id=course_id)
  all_grades = course.grade_set.all()
  return render_to_response('courses/grades.html', 
                            { 'all_grades': all_grades, 
                              'course_title': course.title })
