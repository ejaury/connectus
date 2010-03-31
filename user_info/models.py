from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  IMAGE_BASE_PATH = '/site_media/images/users'

  user = models.ForeignKey(User, unique=True)
  gender = models.CharField(max_length=50)
  image_path = models.CharField(max_length=100)

  def __unicode__(self):
    return '%s %s' % (self.user.first_name, self.user.last_name)

class ParentStudentRelation(models.Model):
  parent = models.ForeignKey(User, related_name="parent")
  student = models.ForeignKey(User, unique=True, related_name="children")

  def __unicode__(self):
    return '%s %s - %s %s' % (self.parent.first_name, self.parent.last_name, \
                              self.student.first_name, self.student.last_name)

