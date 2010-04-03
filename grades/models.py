from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from connectus.courses.models import Course, CourseRegistration

# Create your models here.
class Gradeable(models.Model):
  name = models.CharField(max_length=100)
  course = models.ForeignKey(Course)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __unicode__(self):
    return '%s - %s' % (self.course.title, self.name)

class Grade(models.Model):
  comment = models.CharField(max_length=250, blank=True, null=True)
  score = models.FloatField()
  gradeable = models.ForeignKey(Gradeable)
  student = models.ForeignKey(User)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return '%s %s - %s' % (self.student.first_name,
                           self.student.last_name,
                           self.gradeable.name)

class GradeForm(ModelForm):
  class Meta:
    model = Grade

  def __init__(self, *args, **kwargs):
    course = kwargs.get('course')
    kwargs.clear()
    super(ModelForm, self).__init__(*args, **kwargs)

    # filter query results
    self.fields['gradeable'].queryset = Gradeable.objects.filter(course=course)
    registered_students = CourseRegistration.objects.filter(course=course)
    student_ids = []
    for reg in registered_students:
      student_ids.append(reg.student.id)
    self.fields['student'].queryset = User.objects.filter(id__in=student_ids) 

    # add CSS class for client-side validation
    self.fields['score'].widget.attrs['class'] = \
      'validate[required,custom[floatOnly],length[0,5]]'
    self.fields['gradeable'].widget.attrs['class'] = 'validate[required]'
    self.fields['student'].widget.attrs['class'] = 'validate[required]'
