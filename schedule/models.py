from django.db import models
from connectus.courses.models import Course

# Create your models here.
class CourseCalendar(models.Model):
  course = models.ForeignKey(Course)
  calendar_id = models.CharField(max_length=100, unique=True)
  # TODO: when schedule is added automatically upon class object creation,
  # 'blank' option must be removed)
  calendar_color = models.CharField(max_length=20, blank=True)

  def __unicode__(self):
    return self.course.title
