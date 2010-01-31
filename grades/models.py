from django.db import models
from django.forms import ModelForm
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
  comment = models.CharField(max_length=250)
  score = models.FloatField()
  gradeable = models.ForeignKey(Gradeable)
  # TODO: These would be ForeignKeys
  student = models.CharField(max_length=50)

  def __unicode__(self):
    return '%s - %s' % (self.student, self.gradeable.name)

class GradeForm(ModelForm):
  class Meta:
    model = Grade

