from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from connectus.courses.models import Course

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
    super(ModelForm, self).__init__(*args, **kwargs)
    # add CSS class for client-side validation
    self.fields['score'].widget.attrs['class'] = \
      'validate[required,custom[onlyNumber],length[0,5]]'
    self.fields['gradeable'].widget.attrs['class'] = 'validate[required]'
    self.fields['student'].widget.attrs['class'] = 'validate[required]'
