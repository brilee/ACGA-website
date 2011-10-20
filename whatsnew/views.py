from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404

def whatsnew(request):
	return render_to_response('whatsnew.html', {'NavID': 'whatsnew', 'sidebar': 'sidebar2.html'})
