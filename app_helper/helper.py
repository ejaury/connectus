from django import forms 

class DateForm(forms.Form):
  date = forms.DateField()

class LoginForm(forms.Form):
  username = forms.CharField(max_length=30)
  password = forms.CharField(widget=forms.PasswordInput(render_value=False))

# Hardcoded navigation tree - this should've been in DB
class NavigationTree():
  teacher_class_detail = {
    'Attendance': {
      'id': 'view_attendance',
      'icon_path': 'attendance.png',
    },
    'Grades': {
      'id': 'view_grades',
      'icon_path': 'grades.png',
    },
    'Gradeables': {
      'id': 'view_gradeables',
      'icon_path': 'gradeables.png',
    },
    'Seating Plan': {
      'id': 'view_seating_plan',
      'icon_path': 'seating_plan.png',
    },
    'Submissions': {
      'id': 'view_submissions',
      'icon_path': 'submissions.png',
    },
  }

  student_class_detail = {
    'Grades': {
      'id': 'view_own_grades',
      'icon_path': 'grades.png',
    },
    'Submissions': {
      'id': 'view_submissions',
      'icon_path': 'submissions.png',
    },
  }

  @staticmethod
  def get_class_detail(group):
    if group:
      if group[0].name == 'Student':
        return NavigationTree.student_class_detail
      elif group[0].name == 'Teacher':
        return NavigationTree.teacher_class_detail
    else:
      return None
