from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from CGA.forms import ProfileForm

@login_required
def profile(request):
    user = request.user
    email = user.email
    u_p = user.get_profile()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            u_p.description = request.POST.get('description','')
            u_p.club = request.POST.get('club','')
            u_p.handles = request.POST.get('handles','')
            u_p.aga = request.POST.get('aga','')
            u_p.save()
            update = True
        else:
            update = False
        return render_to_response('profile.html', {'form':form, 'user':user, 'update':update, 'email':email})
    else:
        username = u_p.user
        description = u_p.description
        club = u_p.club
        handles = u_p.handles
        aga = u_p.aga
        data = {'username':username,
                'email':email,
                'description':description,
                'club':club,
                'handles':handles,
                'aga':aga}
        form = ProfileForm(data)
        return render_to_response('profile.html', {'form':form, 'user':user, 'email':email})
