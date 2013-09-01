from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from accounts.forms import EditPlayerForm, PlayerLinkRequestForm
from accounts.models import PendingPlayerLinkRequest, SchoolEditPermission

@login_required
def display_user_info(request):
    try:
        player = request.user.get_profile()
    except:
        pass
    return render(request, 'user_info.html', locals())

@login_required
def edit_profile_info(request):
    try:
        player = request.user.get_profile()
    except:
        return HttpResponseRedirect('/accounts/profile/')

    if request.method == 'POST': 
        form = EditPlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = EditPlayerForm(instance=player) # An unbound form

    return render(request, 'edit_player_info.html', locals())

@login_required
def link_to_player(request):
    if request.method == 'POST':
        form = PlayerLinkRequestForm(request.POST)
        if form.is_valid():
            player = form.cleaned_data['player']
            user = request.user
            new_link_request = PendingPlayerLinkRequest(player=player, user=user)
            new_link_request.save()
            return HttpResponseRedirect('/accounts/edit/player_link/done')
    else:
        form = PlayerLinkRequestForm()

    return render(request, 'create_link_request.html', locals())

@login_required
def display_all_link_requests(request):
    authorized_schools = [perm.school for perm in SchoolEditPermission.objects.filter(
                            user=request.user)]
    all_requests = PendingPlayerLinkRequest.objects.all()
    relevant_requests = [r for r in all_requests
                           if any(r.player in s.player_set.all()
                                  for s in authorized_schools)]
    return render(request, 'all_link_requests.html', locals())

@login_required
def display_link_request(request, link_request_id):
    link_request = PendingPlayerLinkRequest.objects.get(id=link_request_id)

    return render(request, 'link_request.html', locals())
