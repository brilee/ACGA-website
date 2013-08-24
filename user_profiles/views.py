from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from forms import ProfileForm

@login_required
def profile(request):
    user = request.user
    u_p = request.user.get_profile()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            print('valid ProfileForm')
            u_p.description = form['description']
            u_p.club = form['club']
            u_p.handles = form['handles']
            u_p.aga = form['aga']
            update = True
        else:
            update = False
        return render_to_response('profile.html', {'form':form, 'user':user, 'update':update, 'email':u_p.email})
    else:
        username = u_p.user
        email = u_p.email
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
        return render_to_response('profile.html', {'form':form, 'user':user})

