import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from connectus.app_helper.helper import Util
from connectus.courses.models import Course, CourseRegistration
from connectus.grades.models import Grade, Gradeable
from connectus.user_info.models import ParentStudentRelation

@login_required
def index(req):
  if Util.is_in_group(req.user, 'Parent'): 
    relations = ParentStudentRelation.objects.filter(parent=req.user) 
    children = []
    for rel in relations:
      children.append(rel.student)
    children_grades = {} 
    for child in children:
      registrations = CourseRegistration.objects.filter(student=child)
      #
      # grades_by_class: {
      #   'class 1': {
      #     'grades': [34.5, null],
      #     'avg': "[34.5, 50.6]",
      #     'labels: "['Assignment 1', 'Asgn 2']
      #   }
      # }
      #
      grades_by_class = {}
      for reg in registrations:
        grades_by_class[reg.course.title] = {} 
        grades = Grade.objects.filter(gradeable__course=reg.course,
                                      student=child).\
                               order_by('created_at')
        gradeables = Gradeable.objects.filter(course=reg.course).\
                                       order_by('created_at')
        
        # create list of all grades by this student on this class
        x_labels = []
        grade_list = []
        for gradeable in gradeables:
          score = __get_score(gradeable, grades)
          grade_list.append(score)
          x_labels.append(gradeable.name)

        # calc class avg ordered by gradeables
        cls_avg = [] 
        for gradeable in gradeables:
          all_grades = Grade.objects.filter(gradeable=gradeable,
                                            gradeable__course=reg.course)
          sum_grades = 0
          for grade in all_grades:
            sum_grades += grade.score
          avg = sum_grades / len(all_grades)
          cls_avg.append(avg)

        # need to serialize to JSON format
        grades_by_class[reg.course.title]['grades'] = json.dumps(grade_list)
        grades_by_class[reg.course.title]['avg'] = json.dumps(cls_avg)
        grades_by_class[reg.course.title]['labels'] = json.dumps(x_labels)

      children_grades[child] = grades_by_class

      # For now, let's just return grade's of one child
      return render_to_response('stats/index.html', {
                                  'student': child,
                                  'grades_by_class': grades_by_class,
                                },
                                context_instance=RequestContext(req))
  else:
    #TODO: return error message here
    return HttpResponseRedirect('/')

def __get_score(gradeable, grades):
  # TODO: find a faster way of lookup
  for grade in grades:
    if grade.gradeable == gradeable:
      return grade.score
  return None
