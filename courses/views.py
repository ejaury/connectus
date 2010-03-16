import datetime
import json
import random
from copy import deepcopy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from connectus.courses.models import Course, CourseRegistration, Attendance
from connectus.grades.models import Grade, GradeForm
from connectus.user_info.models import UserProfile

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
  if req.is_ajax():
    date = datetime.date.today() - datetime.timedelta(1)
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
                                'course_title': Course.objects.get(id=course_id).title,
                                'date': date.strftime("%A, %B %d, %Y"),
                              },
                              context_instance=RequestContext(req))

def update_grades(req, course_id):
  if req.method == 'POST':
    grade = Grade.objects.get(id=req.POST['id'])

    if grade:
      grade.score = req.POST['value']
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
