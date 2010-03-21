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
    # only student is allowed to check this
    if req.user.is_authenticated():
      student_group = Group.objects.get(name='Student')
      if student_group in req.user.groups.all():
        course = Course.objects.get(id=course_id)
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
    else:
      # redirect to login page
      # special case: use this method to redirect instead of login_required
      #               decorator when request is ajax
      return HttpResponse('/accounts/login/', status=302)

    return render_to_response(template_name, {
                                'course_title': course.title,
                                'course_id': course_id,
                                'submissions': submissions,
                              },
                              context_instance=RequestContext(req))

def update_uploaded(req, course_id):
  FileUploadFormSet = formset_factory(AssignmentFileUploadForm)
  if req.is_ajax:
    if req.method == 'POST':
      formset = FileUploadFormSet(req.POST, req.FILES)
      if formset.is_valid():
        print 'valid'
      print formset
      return HttpResponse()
