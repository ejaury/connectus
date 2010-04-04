from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from connectus.app_helper.helper import LoginForm, Util
from connectus.user_info.models import ParentStudentRelation

@login_required
def index(req):
  children = None
  if Util.is_in_group(req.user, 'Parent'):
    relations = ParentStudentRelation.objects.filter(parent=req.user).\
                                              order_by('student')
    children = []
    for rel in relations:
      children.append(rel.student)
    
  return render_to_response('main/index.html', {
                              'children': children,
                            },
                            context_instance=RequestContext(req))

def login_user(request):
  form = LoginForm()
  if request.method == 'POST':
    next = request.GET.get('next')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        print "NEXT"
        print next
        if next:
          return HttpResponseRedirect(next)
        else:
          return HttpResponseRedirect('/')
        # Redirect to a success page.
      else:
        print 'DISABLED ACC'
        # Return a 'disabled account' error message
    else:
      print 'INVALID LOGIN'
      # Return an 'invalid login' error message.

  return render_to_response('main/login.html',
                            { 'form': form },
                            context_instance=RequestContext(request))
