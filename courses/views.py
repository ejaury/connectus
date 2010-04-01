import datetime
import json
import random
import re
from copy import deepcopy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from connectus.app_helper.helper import DateForm, NavigationTree, Util, \
                                        ViewMenuMapping
from connectus.courses.models import Course, CourseRegistration, Attendance
from connectus.grades.models import Grade, Gradeable, GradeForm
from connectus.user_info.models import UserProfile
from urlparse import urlparse

@login_required
def index(req):
  # Default is teacher
  all_courses = Course.objects.all().order_by('-id')
  if Util.is_in_group(req.user, 'Student'):
    registered_courses = \
      CourseRegistration.objects.filter(student__id=req.user.id)
    course_ids = []
    for reg in registered_courses:
      course_ids.append(reg.course.id) 
    all_courses = Course.objects.filter(id__in=course_ids)
    
  return render_to_response('courses/index.html',
                            { 'all_courses': all_courses },
                            context_instance=RequestContext(req))

@login_required
def detail(req, course_id):
  default_url = req.GET.get('url')
  default_selected_id = "view_grades"
  if not default_url:
    default_url = reverse('connectus.courses.views.grades',
                          args=[course_id])
    if Util.is_in_group(req.user, 'Student'):
      default_url = reverse('connectus.courses.views.view_own_grades',
                            args=[course_id])

  try:
    view_func, args, kwargs = resolve(default_url)
    view_name = Util.construct_module_name(view_func)
    selected_cls_menu_id = \
      ViewMenuMapping.class_submenu_mapping.get(view_name, default_selected_id)
  except:
    selected_cls_menu_id = default_selected_id 

  course = Course.objects.get(id=course_id)
  #TODO: change default by passing view name through GET param
  permitted_actions = NavigationTree.get_class_detail(req.user.groups.all())
  return render_to_response('courses/grades.html', {
                              'course_id': course_id,
                              'course_title': course.title,
                              'default_url': default_url,
                              'permitted_actions': permitted_actions,
                              'selected_cls_menu_id': selected_cls_menu_id,
                            },
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

@login_required
def view_own_grades(req, course_id):
  course = Course.objects.get(id=course_id)

  if req.is_ajax():
    groups = req.user.groups.all()
    if groups and groups[0].name == 'Student':
      grades = Grade.objects.filter(gradeable__course__id=course_id,
                                    student__id=req.user.id) 
      return render_to_response('courses/view_own_grades.html', {
                                  'course_id': course_id,
                                  'course_title': course.title,
                                  'grades': grades,
                                },
                                context_instance=RequestContext(req))

def view_seating_plan(req, course_id):
  profile_img_basepath = UserProfile.IMAGE_BASE_PATH
  max_seats = 20
  if req.is_ajax():
    course = Course.objects.get(id=course_id)
    # TODO: Order ascendingly by student's registration time
    registered_students = course.students.all()
    reg_info = CourseRegistration.objects.filter(course=course.id)
    seating_left = [] 
    seating_right = [] 

    if len(reg_info) > max_seats:
      raise AssertionError('Number of students registered in class %i exceeds \
        class capacity which is %i' % (len(reg_info), max_seats))

    if not course.seat_order.strip():
      # no ordering, initialize
      order = range(max_seats)
      serialized_order = json.dumps(order)
      course.seat_order = serialized_order
      course.save()

      # init seat number
      pos = 0
      for student in reg_info:
        student.seat_number = pos
        student.save()
        pos += 1

    order = json.loads(course.seat_order)

    # populate currently occupied seat numbers
    current_seat_numbers = []
    for info in reg_info:
      if info.seat_number:
        current_seat_numbers.append(info.seat_number)

    seat_num_student_pair = {}

    for info in reg_info:
      if info.seat_number:
        seat_num_student_pair[info.seat_number] = info.student
      else:
        # crude way to choose an available seat number
        # if seat number has not been assigned
        while True:
          info.seat_number = random.randint(0, max_seats - 1)
          if info.seat_number not in current_seat_numbers:
            info.save()
            seat_num_student_pair[info.seat_number] = info.student
            break

    counter = 0
    for seat_num in order:
      student = seat_num_student_pair.get(seat_num)

      if student:
        seat_info = (seat_num, student)
      else:
        seat_info = (seat_num,)

      if (counter < (max_seats / 2)):
        seating_left.append(seat_info)
      else:
        seating_right.append(seat_info)

      counter += 1

    return render_to_response('courses/view_seating_plan.html', {
                                'course': course,
                                'profile_img_basepath': profile_img_basepath,
                                'seating_left': seating_left,
                                'seating_right': seating_right,
                              },
                              context_instance=RequestContext(req))

def attendance(req, course_id):
  print req.method
  if req.is_ajax():
    form = DateForm()
    update = False
    if req.method == 'POST':
      date = req.POST.get('date')
      date = datetime.datetime.strptime(date, '%Y-%m-%d')
      update = True
    else:
      # TODO: change this to Today's date
      date = datetime.date.today()

    s_attending = Attendance.objects.filter(course__id=course_id, date=date)
    s_registered = CourseRegistration.objects.filter(course__id=course_id)
    attendance_d = {} 
    for att in s_attending: 
      attendance_d[att.student] = True
    for reg in s_registered:
      if reg.student not in attendance_d:
        attendance_d[reg.student] = False

    attendance = [] 
    for student,att in attendance_d.items():
      attendance.append((student, att))
    attendance.sort(__user_tuple_compare)

    return render_to_response('courses/view_attendance.html', {
                                'attendance': attendance,
                                'course_id': course_id,
                                'course_title': Course.objects.get(id=course_id).title,
                                'date': date.strftime("%A, %B %d, %Y"),
                                'form': form,
                                'update': update,
                              },
                              context_instance=RequestContext(req))

def update_grades(req, course_id):
  if req.method == 'POST':
    try:
      ids = req.POST['id'].split('-')
      grade_id = re.findall('[\d]+$', ids[2])[0]
      grade = Grade.objects.get(id=grade_id)
      grade.score = req.POST['value']
      grade.save()

    except:
      # grade doesn't exist yet, create one
      uid = ids[0].strip('uid_')
      student = User.objects.get(id=uid)
      gradeable_id = ids[1].strip('gradeable_')
      gradeable = Gradeable.objects.get(id=gradeable_id)
      grade = Grade(student=student,
                    gradeable=gradeable,
                    score=req.POST['value'])
      grade.save()

    return HttpResponse(float(grade.score))

def update_seating_order(req, course_id):
  if req.is_ajax():
    course = Course.objects.get(id=course_id)
    new_seat_order = [] 

    if req.GET.getlist('seat[]'):
      #convert to int
      for order in req.GET.getlist('seat[]'):
        new_seat_order.append(int(order))

      course.seat_order = json.dumps(new_seat_order)
      course.save()

    return HttpResponse()

def __user_tuple_compare(a, b):
  x = '%s %s' % (a[0].first_name, a[0].last_name)
  y = '%s %s' % (b[0].first_name, b[0].last_name)
  if x > y:
    return 1
  elif x == y:
    return 0
  else:
    return -1
