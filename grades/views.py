from django.shortcuts import get_object_or_404, render_to_response
from connectus.grades.models import Grade
from connectus.courses.models import Course

def index(req):
  all_grades = Grade.objects.all().order_by('-id')
  return render_to_response('grades/index.html', {'all_grades': all_grades})

def list_by_course(req, course_id):
  course_obj = Course.objects.get(id=course_id)
  grades_by_course = Grade.objects.filter(course=course_obj).order_by('-id')
  return render_to_response('grades/list_by_course.html',  
                            {'grades_by_course': grades_by_course})
  
def detail(req, grade_id):
  grade = get_object_or_404(Grade, pk=grade_id)
  return render_to_response('grades/detail.html', {'grade': grade})
