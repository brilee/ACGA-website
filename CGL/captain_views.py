from django.shortcuts import render, get_object_or_404

from CGL.models import Match, Season, Player
from CGL.settings import current_seasons
from CGL.captain_auth import school_auth_required, get_school
from CGL.forms import SubmitRosterInformationForm

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
    return render(request, 'edit-matches.html', locals())

@school_auth_required
def display_match(request, match_id):
    school = get_school(request)
    all_players = Player.objects.filter(school=school)
    match = get_object_or_404(Match, id=match_id)
    games = match.game_set.all().order_by("board")
    player_attr = "team1_player" if match.team1.school == school else "team2_player"
    if request.method == 'POST':
        # Got information; handle it
        form = SubmitRosterInformationForm(request.POST)
        if form.is_valid():
            for i in "123":
                player_name = form.cleaned_data['player_name'+i]
                player_is_new = form.cleaned_data['player_is_new'+i]
                if player_is_new:
                    player = Player.objects.get_or_create(school=school, name=player_name)[0]
                else:
                    player = Player.objects.get(school=school, name=player_name)
                game = match.game_set.get(board=i)
                setattr(game, player_attr, player)
                game.save()
    else:
        # Hitting page for first time; prepopulate fields
        players = [getattr(game, player_attr) for game in games]
        form = SubmitRosterInformationForm(initial=dict(
            player_name1=players[0].name,
            player_name2=players[1].name,
            player_name3=players[2].name,
            school_name=school.name
        ))

    return render(request, 'edit-matches-detailed.html', locals())
    