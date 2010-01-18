from django.db import models
from connectus.courses.models import Course

# Create your models here.
class Grade(models.Model):
  comment = models.CharField(max_length=250)
  score = models.FloatField() 
  course = models.ForeignKey(Course) 
  # TODO: These would be ForeignKeys
  gradeable = models.CharField(max_length=50)
  student = models.CharField(max_length=50)

  def __unicode__(self):
    return self.gradeable

"""
class Gradeable(models.Model):
  pass
"""
