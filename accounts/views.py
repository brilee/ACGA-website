from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from accounts.forms import EditPlayerForm, EditSchoolForm, PlayerLinkRequestForm, ApproveLinkRequestForm
from accounts.models import PendingPlayerLinkRequest, SchoolEditPermission
from CGL.models import School, Player

@login_required
def display_user_info(request):
    try:
        player = request.user.get_profile()
    except:
        pass

    school_edit_permissions = SchoolEditPermission.objects.get_all_schools(request.user)

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
        form = EditPlayerForm(instance=player)

    return render(request, 'edit_player_info.html', locals())

@login_required
def create_player(request, school_slug):
    school = School.objects.get(slug_name=school_slug)
    if school in SchoolEditPermission.objects.get_all_schools(request.user):        
        if request.method == 'POST': 
            form = EditPlayerForm(request.POST)
            if form.is_valid():
                args = form.cleaned_data.copy()
                args['school'] = school
                Player.objects.create(**args)
                return HttpResponseRedirect('/accounts/edit/school/%s/' % school_slug)
        else:
            form = EditPlayerForm()
        return render(request, 'create_player.html', locals())
    else:
        return HttpResponseRedirect('/accounts/profile/')

@login_required
def edit_player_info(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if SchoolEditPermission.objects.has_edit_permissions(request.user, player):
        if request.method == 'POST': 
            form = EditPlayerForm(request.POST, instance=player)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/accounts/profile/')
        else:
            form = EditPlayerForm(instance=player)

        return render(request, 'edit_player_info.html', locals())
    else:
        return HttpResponseRedirect('/accounts/profile/')

    
@login_required
def edit_school_info(request, school_slug):
    school = get_object_or_404(School, slug_name=school_slug)
    if school in SchoolEditPermission.objects.get_all_schools(request.user):
        if request.method == 'POST': 
            form = EditSchoolForm(request.POST, instance=school)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/accounts/profile/')
        else:
            form = EditSchoolForm(instance=school)
        return render(request, 'edit_school_info.html', locals())

    else:
        return HttpResponseRedirect('/accounts/profile/')

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
    all_requests = PendingPlayerLinkRequest.objects.all()
    relevant_requests = [r for r in all_requests
            if SchoolEditPermission.objects.has_edit_permissions(request.user, r.player)]
    return render(request, 'all_link_requests.html', locals())

@login_required
def display_link_request(request, link_request_id):
    link_request = PendingPlayerLinkRequest.objects.get(id=link_request_id)
    if SchoolEditPermission.objects.has_edit_permissions(request.user, link_request.player):
        if request.method == 'POST':
            form = ApproveLinkRequestForm(request.POST, instance=link_request)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/accounts/link_requests/')
        else:
            form = ApproveLinkRequestForm(instance=link_request)

        return render(request, 'approve_link_request.html', locals())
    else:
        return HttpResponseRedirect('/accounts/link_requests/')
