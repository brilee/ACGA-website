import json

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from CGL.models import Season, Match, Game, Player, School
from CGL.settings import current_seasons
from CGL.captain_auth import school_auth_required, get_school, check_auth
from CGL.forms import EditSchoolForm, EditPlayerForm

@school_auth_required
def edit_all_matches(request):
    school = get_school(request)

    season_matches = Match.objects.none()
    for season in (Season.objects.get(name=s) for s in current_seasons):
        season_matches = season_matches | Match.objects.filter(round__season=season)

    relevant_matches = [m for m in season_matches
            if m.round.in_past()
            and (m.team1.school == school
                 or m.team2.school == school)]
    return render(request, 'matches.html', locals())

@school_auth_required
def edit_match(request, match_id):
    school = get_school(request)
    all_players = Player.objects.filter(school=school)
    match = get_object_or_404(Match, id=match_id)
    school_is_team1 = match.team1.school == school
    return render(request, 'matches-detailed.html', locals())

@school_auth_required
def edit_school(request, school_slug):
    school_authed = get_school(request)
    school = get_object_or_404(School, slug_name=school_slug)
    if not check_auth(school_authed, school):
        raise PermissionDenied

    if request.method == 'POST':
        form = EditSchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
    else:
        form = EditSchoolForm(instance=school)
    return render(request, 'edit_school.html', locals())

@school_auth_required
def edit_player(request, player_id):
    school = get_school(request)
    player = get_object_or_404(Player, id=player_id)
    if not check_auth(school, player):
        raise PermissionDenied

    if request.method == 'POST':
        form = EditPlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
    else:
        form = EditPlayerForm(instance=player)
    return render(request, 'edit_player.html', locals())
    
@require_http_methods(["PUT"])
@school_auth_required
def update_players(request, game_id):
    school = get_school(request)
    game = get_object_or_404(Game, id=game_id)
    if not check_auth(school, game):
        raise PermissionDenied
    submitted_data = json.loads(request.body)
    try:
        player = Player.objects.get(name=submitted_data['player_name'], school=school)
    except Player.DoesNotExist:
        return HttpResponseBadRequest('Couldn\'t find player')

    if game.match.team1.school == school:
        game.team1_player = player
    else:
        game.team2_player = player

    game.save()

    return HttpResponse("success")
