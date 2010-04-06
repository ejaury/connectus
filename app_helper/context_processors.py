from django.core.urlresolvers import reverse, resolve, NoReverseMatch
from connectus.app_helper.helper import NavigationTree, Util, ViewMenuMapping
from connectus.courses.models import Course, CourseRegistration

def sidebar(request):
  # TODO: order by course title
  if request.user.is_anonymous():
    return {}

  user_groups = request.user.groups.all()
  if user_groups:
    menus = NavigationTree.get_main_navi(user_groups)
  else:
    return {} 

  # check inbox
  unread_msg = Util.get_num_unread_msg(request.user)
  
  #TODO need a better way to check for groups
  if user_groups[0].name == 'Teacher': 
    #TODO: check which class this teacher belongs to 
    courses = Course.objects.all()
  elif user_groups[0].name == 'Student':
    regs = CourseRegistration.objects.filter(student=request.user)
    course_ids = []
    for reg in regs:
      course_ids.append(reg.course.id)
    courses = Course.objects.filter(id__in=course_ids)
  else:
    courses = []

  return {
    'courses': courses,
    'menus': menus,
    'unread_msg': unread_msg,
  }

def navigation_view_solver(request):
  view_func, args, kwargs = resolve(request.path)
  view_name = Util.construct_module_name(view_func)
  selected_id = ViewMenuMapping.mapping.get(view_name, '')
  # construct navigation tree path
  tree_path = NavigationTree.get_nav_tree_path(view_name)
  reversed_tree_path = reverse_path(tree_path, kwargs.values())
  # presumably, if we can't find a path for this view, we're actually
  # coming from a view that we recognize 
  if not reversed_tree_path:
    last = NavTreeState.get_last()
    # worse case, we can't recognize a view name and we dont have any prev state
    # use Home in tree 
    reversed_tree_path = last if last else [('Home', '/')] 
  else:
    NavTreeState.save(reversed_tree_path)
  if kwargs and selected_id.endswith('_'):
    if len(kwargs) == 1:
      selected_id += kwargs.values()[0]
  return {
    'selected_id': selected_id,
    'tree_path': reversed_tree_path,
  }

def reverse_path(path, args):
  if path:
    reversed_path = []
    for i,node in enumerate(path):
      try:
        url = reverse(node.view_name, args=args)
      except NoReverseMatch:
        url = reverse(node.view_name)
      #hack: construct ajax path
      if i == 3:
        url = '%s?url=%s' % (reversed_path[2][1], url)
      #hack: give name to course node
      if node.view_name == 'connectus.courses.views.detail':
        course = Course.objects.get(id=args[0])
        node.name = course.title
      reversed_path.append((node.name, url))
    return reversed_path

#hack: nav tree state saving
class NavTreeState:
  last_tree_path = None

  @classmethod
  def save(self, last_tree_path):
    self.last_tree_path = last_tree_path

  @classmethod
  def get_last(self):
    return self.last_tree_path

