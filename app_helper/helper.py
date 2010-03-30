from django import forms 

class DateForm(forms.Form):
  date = forms.DateField()

class LoginForm(forms.Form):
  username = forms.CharField(max_length=30)
  password = forms.CharField(widget=forms.PasswordInput(render_value=False))

# Hardcoded navigation tree - this should've been in DB
class NavigationTree():
  main_navi = (
    ('Home', {
      'id': 'sidebar_home',
      'icon_path': 'home.png',
      'url': '/',
    }),
    ('Classes', {
      'id': 'sidebar_class',
      'icon_path': 'class.png',
      'url': '/courses',
    }),
    ('Calendar', {
      'id': 'sidebar_calendar',
      'icon_path': 'calendar.png',
      'url': '/schedule/view',
    })
  )

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
  def get_main_navi(group):
    if group:
      if group[0].name == 'Teacher':
        return NavigationTree.main_navi
      elif group[0].name == 'Student':
        return NavigationTree.main_navi
    else:
      return None

  @staticmethod
  def get_class_detail(group):
    if group:
      if group[0].name == 'Student':
        return NavigationTree.student_class_detail
      elif group[0].name == 'Teacher':
        return NavigationTree.teacher_class_detail
    else:
      return None

class ViewMenuMapping:
  # available options in main menu
  # pair of view name and HTML list id
  # the list id MUST match those defined in NavigationTree
  mapping = {
    'connectus.main.views.index': 'sidebar_home',
    'connectus.courses.views.index': 'sidebar_class',
    'connectus.schedule.views.view': 'sidebar_calendar',
    'connectus.courses.views.detail': 'view_course_',
    'connectus.courses.views.attendance': 'view_course_',
    'connectus.courses.views.grades': 'view_course_',
    'connectus.courses.views.view_seating_plan': 'view_course_',
    'connectus.submissions.views.view_uploaded': 'view_course_',
    'connectus.submissions.views.view_submissions': 'view_course_',
  }

  class_submenu_mapping = {
    'connectus.courses.views.attendance': 'view_attendance',
    'connectus.courses.views.grades': 'view_grades',
    'connectus.courses.views.view_own_grades': 'view_own_grades',
    'connectus.courses.views.view_seating_plan': 'view_seating_plan',
    'connectus.submissions.views.view_uploaded': 'view_gradeables',
    'connectus.submissions.views.view_submissions': 'view_submissions',
  }

class Util:
  @staticmethod
  def construct_module_name(function):
    try:
      name = '%s.%s' % (function.__module__, function.func_name)
    except:
      # presumably, this is a CheckLogin obj
      # retrieve func name first
      function = function.view_func
      name = '%s.%s' % (function.__module__, function.func_name)
    return name
