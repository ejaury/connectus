from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  gender = models.CharField(max_length=50)
  image_path = models.CharField(max_length=100)

  def __unicode__(self):
    return '%s %s' % (self.user.first_name, self.user.last_name)
