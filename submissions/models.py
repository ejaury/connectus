from django.contrib.auth.models import User
from django.db import models
from connectus.grades.models import Gradeable

class GradeableFileUpload(models.Model):
  gradeable = models.ForeignKey(Gradeable)
  # TODO: group course and gradeable into subdirectories
  file = models.FileField(upload_to='assignments')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

class StudentSubmission(GradeableFileUpload):
  student = models.ForeignKey(User)
  submission_date = models.DateTimeField()

class AssignmentFileUpload(GradeableFileUpload):
  due_date = models.DateTimeField()
