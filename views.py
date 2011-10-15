from django.shortcuts import render_to_response
from django.http import HttpResponse

def home(request):
	return render_to_response('index.html')


#def current_datetime(request):
#	current_date = datetime.datetime.now()
#	return render_to_response('index.html',locals())

def whatsnew(request):
	return render_to_response('sidebar.html')

def stylesheet(request):
	return HttpResponse('style.css')