import json

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

from CGL.models import Season, Match, Game, Player
from CGL.settings import current_seasons
from CGL.captain_auth import school_auth_required, get_school

@school_auth_required
def display_all_matches(request):
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
def display_match(request, match_id):
    school = get_school(request)
    all_players = Player.objects.filter(school=school)
    match = get_object_or_404(Match, id=match_id)
    school_is_team1 = match.team1.school == school
    return render(request, 'matches-detailed.html', locals())
    
@require_http_methods(["PUT"])
@school_auth_required
def update_players(request, game_id):
    school = get_school(request)
    game = get_object_or_404(Game, id=game_id)
    if not (game.match.team1.school == school or game.match.team2.school == school):
        return HttpResponseBadRequest("Don't have auth for that school")
    submitted_data = json.loads(request.body)
    if submitted_data.get("is_new_player"):
        player = Player.objects.get_or_create(school=school, name=submitted_data['player_name'])[0]
    else:
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
