from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404

def images(request):
	return render_to_response('images.html', {'NavID': 'images', 'sidebar': 'sidebar.html'})
