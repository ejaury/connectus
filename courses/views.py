from django.shortcuts import get_object_or_404, render_to_response
from connectus.courses.models import Course
from connectus.grades.models import GradeForm

def index(req):
  all_courses = Course.objects.all().order_by('-id')
  return render_to_response('courses/index.html', { 'all_courses': all_courses})

def grades(req, course_id):
  course = Course.objects.get(id=course_id)
  by_student = {}
  all_gradeables = course.gradeable_set.all()

  for gradeable in all_gradeables:
    all_grades = gradeable.grade_set.all()

    for grade in all_grades:
      if not by_student.get(grade.student, None):
        by_gradeable = {}
        by_gradeable[gradeable.name] = grade
        by_student[grade.student] = by_gradeable
      else:
        by_student[grade.student][gradeable.name] = grade 

  return render_to_response('courses/grades.html', 
                            { 'all_gradeables': all_gradeables, 
                              'grades_by_student': by_student,
                              'course_title': course.title })
