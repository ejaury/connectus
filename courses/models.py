from django.db import models

# Create your models here.
class Course(models.Model):
  title = models.CharField(max_length=50)
  description = models.CharField(max_length=200)
  term = models.CharField(max_length=10)
  year = models.IntegerField()

  def __unicode__(self):
    return self.title
