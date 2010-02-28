from copy import deepcopy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from connectus.courses.models import Course
from connectus.grades.models import Grade, GradeForm

def index(req):
  all_courses = Course.objects.all().order_by('-id')
  return render_to_response('courses/index.html',
                            { 'all_courses': all_courses },
                            context_instance=RequestContext(req))

def grades(req, course_id):
  course = Course.objects.get(id=course_id)

  if req.is_ajax():
    all_gradeables = course.gradeable_set.all()
    by_student = {}
    gradeables_length = len(all_gradeables)

    for gradeable in all_gradeables:
      all_grades = gradeable.grade_set.all()

      for grade in all_grades:
        if not by_student.get(grade.student, None):
          by_gradeable = {}
          by_gradeable[gradeable.name] = grade
          by_student[grade.student] = by_gradeable
        else:
          by_student[grade.student][gradeable.name] = grade

    # Hack due to Django's limitation on accessing dictionary
    # within a dictionary:
    # Fill in empty Gradeable with something
    by_student_copy = deepcopy(by_student)
    for student,existing_gradeables in by_student_copy.iteritems():
      for gradeable in all_gradeables:
        if not existing_gradeables.get(gradeable.name, None):
          by_student[student][gradeable.name] = 'N/A'

    context_data = {
      'all_gradeables': all_gradeables,
      'gradeables_length': gradeables_length,
      'grades_by_student': by_student,
      'course_title': course.title,
      'course_id': course.id
    }

    template_path = 'courses/grades_ajax.html'

  else:
    context_data = {
      'course_title': course.title,
      'course_id': course.id
    }

    template_path = 'courses/grades.html'

  return render_to_response(template_path,
                            context_data,
                            context_instance=RequestContext(req))

def view_seating_plan(req, course_id):
  course = Course.objects.get(id=course_id)
  if req.is_ajax():
    return render_to_response('courses/view_seating_plan.html', {
                                'course': course
                              },
                              context_instance=RequestContext(req))

def update_grades(req, course_id):
  if req.method == 'POST':
    grade = Grade.objects.get(id=req.POST['id'])

    if grade:
      grade.score = req.POST['value']
      grade.save()

      return HttpResponse(float(grade.score))
