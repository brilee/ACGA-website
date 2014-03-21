from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from accounts.forms import *
from accounts.models import *
from CGL.models import School, Player, Match, Game, Forfeit
from CGL.settings import current_seasons

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
            permissioncheck,
            modelinstance,
            modelform,
            template_name,
            form_valid=None,
            success_redirect='/accounts/profile/',
            no_permission_redirect='/accounts/profile/',
            **kwargs):
    '''
    Generic model editing logic. Should be fairly self-explanatory.
    If the template needs any extra context variables, they can be
    passed in through **kwargs.
    '''
    if SchoolEditPermission.objects.has_edit_permissions(request.user, permissioncheck):
        if request.method == 'POST':
            form = modelform(request.POST, request.FILES, instance=modelinstance)
            if form.is_valid():
                # Here's a handle for custom method execution. 
                # If you want to do something, pass in a function that
                # takes a form argument and does something to it.
                if form_valid:
                    form_valid(form)
                form.save()
                return HttpResponseRedirect(success_redirect)
        else:
            if modelform == EditGameForm:
                # ugly special casing. I would love to just pass in 
                # **kwargs, but the modelform __init__ method is very
                # picky about what kwargs it expects to see, and 
                # throws errors if it sees something unusual.
                # In the 'match' case, the match is popped from the 
                # kwarg list before calling super.__init__() so that
                # django doesn't complain about it.
                form = modelform(instance=modelinstance, match=kwargs['match'])
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
                 permissioncheck=player,
                 modelinstance=player,
                 modelform=EditPlayerForm,
                 template_name='edit_player_info.html',
                 success_redirect='/accounts/profile/',
                 no_permission_redirect='/accounts/profile/')

@login_required
def edit_school_info(request, school_slug):
    school = get_object_or_404(School, slug_name=school_slug)
    return edit_model_with_permissioncheck(request,
                 permissioncheck=school,
                 modelinstance=school,
                 modelform=EditSchoolForm,
                 template_name='edit_school_info.html',
                 success_redirect='/accounts/profile/',
                 no_permission_redirect='/accounts/profile/',
                 school=school)

@login_required
def edit_player_info(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return edit_model_with_permissioncheck(request,
                 permissioncheck=player,
                 modelinstance=player,
                 modelform=EditPlayerForm,
                 template_name='edit_player_info.html',
                 success_redirect='/accounts/profile/',
                 no_permission_redirect='/accounts/profile/')

@login_required
def edit_game_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    match = game.match
    return edit_model_with_permissioncheck(request,
                 permissioncheck=game,
                 modelinstance=game,
                 modelform=EditGameForm,
                 template_name='edit_game_info.html',
                 success_redirect='/accounts/show/matches/',
                 no_permission_redirect='/accounts/profile/',
                 match=match)
    
@login_required
def edit_forfeit_info(request, forfeit_id):
    forfeit = get_object_or_404(Forfeit, id=forfeit_id)
    match = forfeit.match
    if forfeit.match.round.in_near_past():
        return edit_model_with_permissioncheck(request,
                 permissioncheck=forfeit,
                 modelinstance=forfeit,
                 modelform=EditForfeitForm,
                 template_name='edit_forfeit_info.html',
                 success_redirect='/accounts/profile/',
                 no_permission_redirect='/accounts/profile/',
                 match=match)
    else:
        return HttpResponseRedirect('/accounts/profile/')

@login_required
def edit_link_request(request, link_request_id):
    link_request = PendingPlayerLinkRequest.objects.get(id=link_request_id)
    return edit_model_with_permissioncheck(request,
                 permissioncheck=link_request,
                 modelinstance=link_request,
                 modelform=EditLinkRequestForm,
                 template_name='approve_link_request.html',
                 success_redirect='/accounts/link_requests/',
                 no_permission_redirect='/accounts/profile/')

@login_required
def create_player(request, school_slug):
    school = School.objects.get(slug_name=school_slug)
    # I apologize for this code. Would have used a lambda, but 
    # python wouldn't let me.
    def add_school(school):
        def inner(form):
            form.instance.school = school
            return None
        return inner
    return edit_model_with_permissioncheck(request,
                 permissioncheck=school,
                 modelinstance=None,
                 modelform=EditPlayerForm,
                 form_valid=add_school(school),
                 template_name='create_player.html',
                 success_redirect='/accounts/edit/school/%s' % school_slug,
                 no_permission_redirect='/accounts/profile/',
                 school=school)

@login_required
def create_game(request, match_id):
    match = Match.objects.get(id=match_id)
    def add_match(match):
        def inner(form):
            form.instance.match = match
            return None
        return inner
    return edit_model_with_permissioncheck(request,
                 permissioncheck=match,
                 modelinstance=None,
                 modelform=EditGameForm,
                 form_valid=add_match(match),
                 template_name='create_game.html',
                 success_redirect='/accounts/show/matches/',
                 no_permission_redirect='/accounts/profile/',
                 match=match)

@login_required
def create_forfeit(request, match_id):
    match = Match.objects.get(id=match_id)
    def add_match(match):
        def inner(form):
            form.instance.match = match
            return None
        return inner
    
    return edit_model_with_permissioncheck(request,
                 permissioncheck=match,
                 modelinstance=None,
                 modelform=EditForfeitForm,
                 form_valid=add_match(match),
                 template_name='create_forfeit.html',
                 success_redirect='/accounts/show/matches/',
                 no_permission_redirect='/accounts/profile/',
                 match=match)

@login_required
def display_all_matches(request):
    all_school_perms = SchoolEditPermission.objects.get_all_schools(request.user)
    season_matches = Match.objects.none()
    for season in (Season.objects.get(name=s) for s in current_seasons):
        season_matches = season_matches | Match.objects.filter(round__season=season)

    relevant_matches = [m for m in season_matches
            if m.round.in_past()
            and (m.school1 in all_school_perms
                 or m.school2 in all_school_perms)]
    return render(request, 'all_matches.html', locals())

@login_required
def display_all_link_requests(request):
    all_school_perms = SchoolEditPermission.objects.get_all_schools(request.user)
    all_requests = PendingPlayerLinkRequest.objects.all()
    relevant_requests = [r for r in all_requests
            if r.player.school in all_school_perms]
    return render(request, 'all_link_requests.html', locals())


def create_link_request(request):
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

