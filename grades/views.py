from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from connectus.grades.models import Grade, GradeForm
from connectus.courses.models import Course
from urlparse import urlparse

def index(req):
  all_grades = Grade.objects.all().order_by('-id')
  return render_to_response('grades/index.html',
                            {'all_grades': all_grades},
                            context_instance=RequestContext(req))

def add(req):
  if req.method == 'POST':
    form = GradeForm(req.POST)
    # TODO: Validate form better here
    if form.is_valid():
      form.save()
      # assuming we're coming from a course page
      referer = req.META['HTTP_REFERER']
      path = urlparse(referer).path
      redirect_url = referer + '?url=%sgrades/' % path
      return HttpResponseRedirect(redirect_url)
  else:
    form = GradeForm()

  return render_to_response('grades/add.html',
                            { 'form': form  },
                            context_instance=RequestContext(req))

def edit(req, grade_id):
  grade = get_object_or_404(Grade, pk=grade_id)
  if req.method == 'POST':
    form = GradeForm(req.POST, instance=grade)
    # TODO: Validate form better here, also redirect if not valid
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/grades/')
  else:
    form = GradeForm(instance=grade)
  return render_to_response('grades/edit.html', {
                              'form': form,
                              'grade': grade
                            },
                            context_instance=RequestContext(req))

def list_by_course(req, course_id):
  course_obj = Course.objects.get(id=course_id)
  grades_by_course = Grade.objects.filter(course=course_obj).order_by('-id')
  return render_to_response('grades/list_by_course.html',
                            {'grades_by_course': grades_by_course},
                            context_instance=RequestContext(req))

def detail(req, grade_id):
  grade = get_object_or_404(Grade, pk=grade_id)
  return render_to_response('grades/detail.html',
                            {'grade': grade},
                            context_instance=RequestContext(req))
