from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from connectus.app_helper.helper import LoginForm

def index(req):
  return render_to_response('main/index.html',
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
