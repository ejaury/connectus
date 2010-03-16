from django import forms 

class DateForm(forms.Form):
  date = forms.DateField()

class LoginForm(forms.Form):
  username = forms.CharField(max_length=30)
  password = forms.CharField(widget=forms.PasswordInput(render_value=False))
