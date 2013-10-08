from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from accounts.forms import EditPlayerForm, EditSchoolForm, PlayerLinkRequestForm, EditLinkRequestForm, UsernameReminderForm
from accounts.models import PendingPlayerLinkRequest, SchoolEditPermission
from CGL.models import School, Player


def send_username_reminder(request):
    if request.method == 'POST':
        form = UsernameReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/username_reminder/done/')
        else:
            return render(request, 'username_reminder.html', locals())
    else:
        form = UsernameReminderForm()
        return render(request, 'username_reminder.html', locals())

@login_required
def display_user_info(request):
    try:
        player = request.user.get_profile()
    except:
        pass

    school_edit_permissions = SchoolEditPermission.objects.get_all_schools(request.user)

    return render(request, 'user_info.html', locals())

def edit_model_with_permissioncheck(request,
            modelinstance,
            modelform,
            template_name,
            success_redirect='/accounts/profile/',
            no_permission_redirect='/accounts/profile/',
            **kwargs):
    '''
    Generic model editing logic. Should be fairly self-explanatory.
    If the template needs any extra context variables, they can be
    passed in through **kwargs.
    '''
    if SchoolEditPermission.objects.has_edit_permissions(request.user, modelinstance):
        if request.method == 'POST':
            form = modelform(request.POST, instance=modelinstance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(success_redirect)
        else:
            form = modelform(instance=modelinstance)
        return render(request, template_name, dict(locals().items() + kwargs.items()))
    else:
        return HttpResponseRedirect(no_permission_redirect)

@login_required
def edit_profile_info(request):
    try:
        player = request.user.get_profile()
    except:
        return HttpResponseRedirect('/accounts/profile/')

    return edit_model_with_permissioncheck(request,
                 modelinstance=player,
                 modelform=EditPlayerForm,
                 template_name='edit_player_info.html',
                 success_redirect='/accounts/profile/',
                 no_permission_redirect='/accounts/profile/')

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
    return edit_model_with_permissioncheck(request,
                 modelinstance=player,
                 modelform=EditPlayerForm,
                 template_name='edit_player_info.html',
                 success_redirect='/accounts/profile/',
                 no_permission_redirect='/accounts/profile/')

@login_required
def create_game(request):
    pass

@login_required
def edit_game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return edit_model_with_permissioncheck(request,
                 modelinstance=game,
                 modelform=EditGameForm,
                 template_name='edit_game_info.html',
                 success_redirect='/accounts/profile/',
                 no_permission_redirect='/accounts/profile/')
    
@login_required
def create_forfeit(request, match_id):
    pass

@login_required
def edit_forfeit_info(request, forfeit_id):
    forfeit = get_object_or_404(Forfeit, id=forfeit_id)
    if forfeit.match.round.in_near_past():
        return edit_model_with_permissioncheck(request,
                 modelinstance=forfeit,
                 modelform=EditForfeitForm,
                 template_name='edit_forfeit_info.html',
                 success_redirect='/accounts/profile/',
                 no_permission_redirect='/accounts/profile/')
    else:
        return HttpResponseRedirect('/accounts/profile/')


@login_required
def edit_school_info(request, school_slug):
    school = get_object_or_404(School, slug_name=school_slug)
    return edit_model_with_permissioncheck(request,
                 modelinstance=school,
                 modelform=EditSchoolForm,
                 template_name='edit_school_info.html',
                 success_redirect='/accounts/profile/',
                 no_permission_redirect='/accounts/profile/',
                 school=school)

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
    all_school_perms = SchoolEditPermission.objects.get_all_schools(request.user)
    all_requests = PendingPlayerLinkRequest.objects.all()
    relevant_requests = [r for r in all_requests
            if r.player.school in all_school_perms]
    return render(request, 'all_link_requests.html', locals())

@login_required
def edit_link_request(request, link_request_id):
    link_request = PendingPlayerLinkRequest.objects.get(id=link_request_id)
    return edit_model_with_permissioncheck(request,
                 modelinstance=link_request,
                 modelform=EditLinkRequestForm,
                 template_name='approve_link_request.html',
                 success_redirect='/accounts/link_requests/',
                 no_permission_redirect='/accounts/profile/')
