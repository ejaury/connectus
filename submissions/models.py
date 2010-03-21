from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from connectus.grades.models import Gradeable

class GradeableFileUpload(models.Model):
  gradeable = models.ForeignKey(Gradeable)
  # TODO: group course and gradeable into subdirectories
  file = models.FileField(upload_to='assignments')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

  def __unicode__(self):
    return '%s (%s)' % (self.gradeable.name, self.gradeable.course.title)

class StudentSubmission(GradeableFileUpload):
  student = models.ForeignKey(User)
  submission_date = models.DateTimeField()

  def __unicode__(self):
    return '%s (%s): %s %s' % (self.gradeable.name,
                               self.gradeable.course.title,
                               self.student.first_name,
                               self.student.last_name,)

class AssignmentFileUpload(GradeableFileUpload):
  due_date = models.DateTimeField()

class AssignmentFileUploadForm(ModelForm):
  class Meta:
    model = AssignmentFileUpload
