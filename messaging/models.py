from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from connectus.courses.models import Course

# Rough model of messaging system
class Messaging(models.Model):
  course = models.ForeignKey(Course)
  to = models.ForeignKey(User, related_name="recipient")
  sender = models.ForeignKey(User, related_name="sender")
  subject = models.CharField(max_length=100)
  message = models.TextField(blank=True, null=True)
  read = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return "From '%s %s' to '%s %s'" % (self.sender.first_name,
                                        self.sender.last_name,
                                        self.to.first_name,
                                        self.to.last_name)

class MessageForm(ModelForm):
  class Meta:
    model = Messaging
    exclude = 'read'

  def __init__(self, *args, **kwargs):
    super(ModelForm, self).__init__(*args, **kwargs)
    # add CSS class for client-side validation
    self.fields['to'].widget.attrs['class'] = 'validate[required]'
    self.fields['sender'].widget.attrs['class'] = 'validate[required]'
    self.fields['course'].widget.attrs['class'] = 'validate[required]'
    self.fields['subject'].widget.attrs['class'] = 'validate[required]'
