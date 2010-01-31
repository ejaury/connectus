from django.shortcuts import render_to_response

def index(req):
  return render_to_response('main/index.html')  
