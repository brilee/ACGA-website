from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def membership(request):
	return render_to_response('membership.html', {'NavID': 'membership', 'sidebar': 'sidebar3.html'})

def login_user(request):
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
			return HttpResponseRedirect("/membership/profile/")
		else:	
			
			return render_to_response('login.html', {'NavID': 'membership', 'sidebar': 'sidebar3.html', 'next': 'profile/'})

	else:
		return render_to_response('login.html', {'NavID': 'membership', 'sidebar': 'sidebar3.html'})


#@login_required
def profile(request):
	return render_to_response('profile.html', {'NavID': 'membership', 'sidebar': 'sidebar3.html'})

