from django.template.loader import get_template
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from models import School, Season, Round, Membership, Game, Player
from settings import current_season_nameA

def display_school(request):
    all_schools = School.objects.filter(inCGL=True)
    recent_schools = all_schools.order_by("-id")[:3]

    return direct_to_template(request, 'schools.html', locals())

def display_roster(request, school_name):
    school_name = school_name.strip().replace('_', ' ').replace('-', ' ')
    school = get_object_or_404(School, name=school_name)
    roster = school.player_set.filter(isActive=1).order_by('rank')
    inactives = school.player_set.filter(isActive=0).order_by('rank')
    participating_seasons = Membership.objects.filter(school__name=school_name)

    return direct_to_template(request, 'schools-detailed.html', locals())

def redirect_to_current_season(request):
    current_season = Season.objects.get(name=current_season_nameA)
    return redirect(current_season)
    
def display_season(request, season_name):
    season_name = season_name.strip()
    requested_season = get_object_or_404(Season, slug_name=season_name)
    all_memberships = Membership.objects.filter(season=requested_season).order_by('-num_wins', 'num_losses', '-num_ties', 'num_forfeits')
    all_seasons = Season.objects.all().order_by('-id')

    return direct_to_template(request, 'results.html', locals())

def display_player_search(request):
    query = request.GET.get('query', '')
    errors = []

    if query:
        results = Player.objects.filter(name__icontains=query) | Player.objects.filter(KGS_username__icontains=query)
        
        # If only one player found, automatically redirect to that player's page
        if len(results) == 1:
            return HttpResponseRedirect(results[0].get_absolute_url())

        if not results:
            errors.append('No results')

    return direct_to_template(request, 'players.html', locals())

def display_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return direct_to_template(request, 'players-detailed.html', locals())

def display_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    return direct_to_template(request, 'game-detailed.html', locals())
