from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

@login_required
def display_account_profile(request):
    try:
        player = request.user.get_profile()
        # User has linked account to an existing player
        return redirect(request, 'players-detailed.html', locals())
    except:
        # User has not linked their account to an existing player yet.
        errors = ['You may now select a player to associate your account with. Your request will be forwarded to the team captain to approve.']
        return direct_to_template(request, 'players.html', locals())
