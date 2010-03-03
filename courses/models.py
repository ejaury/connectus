from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
  title = models.CharField(max_length=50)
  description = models.CharField(max_length=200)
  term = models.CharField(max_length=10)
  year = models.IntegerField()
  students = models.ManyToManyField(User, through='CourseRegistration')

  def __unicode__(self):
    return self.title

class CourseRegistration(models.Model):
  course = models.ForeignKey(Course)
  # TODO: should only add user associated with group 'Student'
  student = models.ForeignKey(User)
  created_at = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return '%s - %s %s' % (self.course.title, self.student.first_name,
      self.student.last_name)
