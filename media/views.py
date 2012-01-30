from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404

def media(request):
	print 'media'
	return render_to_response('media.html', {'NavID': 'media', 'sidebar': 'sidebar.html'})
