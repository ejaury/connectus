from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from connectus.courses.models import Course, CourseRegistration
from connectus.grades.models import Gradeable
from connectus.submissions.models import AssignmentFileUpload, \
                                         AssignmentFileUploadForm, \
                                         StudentSubmission

def view_uploaded(req, course_id):
  if req.is_ajax():
    course = Course.objects.get(id=course_id)
    gradeables = Gradeable.objects.filter(course__id=course_id)
    uploaded = AssignmentFileUpload.objects.filter(gradeable__course__id=course_id)
    return render_to_response('submissions/view_uploaded.html', {
                                'course_id': course_id,
                                'course_title': course.title,
                                'uploaded': uploaded,
                              },
                              context_instance=RequestContext(req))

def view_submissions(req, course_id):
  if req.is_ajax():
    if req.user.is_authenticated():
      student_group = Group.objects.get(name='Student')
      teacher_group = Group.objects.get(name='Teacher')
      course = Course.objects.get(id=course_id)

      # student's view
      if student_group in req.user.groups.all():
        registrations = CourseRegistration.objects.filter(student__id=req.user.id)
        registered_course_ids = []
        for reg in registrations:
          registered_course_ids.append(reg.course.id)

        submissions = \
          StudentSubmission.objects.filter(
            gradeable__course__id__in=registered_course_ids,
            student__id=req.user.id
          )
        template_name = 'submissions/view_submissions.html'
        context_vars = {
          'course_title': course.title,
          'course_id': course_id,
          'submissions': submissions,
        }

      # teacher's view
      elif teacher_group in req.user.groups.all():
        registrations = CourseRegistration.objects.filter(course__id=course_id)
        gradeables = Gradeable.objects.filter(course__id=course_id)
        gradeable_names = []
        for gradeable in gradeables:
          gradeable_names.append(gradeable.name)

        submitted = \
          StudentSubmission.objects.filter(gradeable__course__id=course_id)
        template_name = 'submissions/view_submissions_teacher.html'

        submissions = {}
        for reg in registrations:
          student_name = '%s %s' % (reg.student.first_name,
                                    reg.student.last_name)
          submissions[student_name] = {}

        for s in submitted:
          student_name = '%s %s' % (s.student.first_name,
                                    s.student.last_name)
          submissions[student_name][s.gradeable.name] = s.file

        context_vars = {
          'course_title': course.title,
          'course_id': course_id,
          'gradeable_names': gradeable_names,
          'submissions': submissions,
        }

      return render_to_response(template_name, 
                                context_vars,
                                context_instance=RequestContext(req))
    else:
      # redirect to login page
      # special case: use this method to redirect instead of login_required
      #               decorator when request is ajax
      return HttpResponse('/accounts/login/', status=302)

def update_uploaded(req, course_id):
  FileUploadFormSet = formset_factory(AssignmentFileUploadForm)
  if req.is_ajax:
    if req.method == 'POST':
      formset = FileUploadFormSet(req.POST, req.FILES)
      if formset.is_valid():
        print 'valid'
      print formset
      return HttpResponse()
