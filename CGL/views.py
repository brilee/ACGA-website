from django.template import RequestContext
from django.template.loader import get_template
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import School, Season, Round, Membership, Game
from settings import current_season_name

def display_CGL(request):
    return render_to_response('CGL.html',
                              context_instance=RequestContext(request))

def display_roster(request):
    school_name = school_name.strip().replace('_', ' ').replace('-', ' ')
    s = get_object_or_404(School, name=school_name)

    roster = s.player_set.filter(isActive=1).order_by('rank')
    retired = s.player_set.filter(isActive=0)
    
    return render_to_response('member-detailed.html',
                              {'school':s, 'roster':roster, 'retired':retired},
                              context_instance=RequestContext(request))

def display_results(request):
    current_season = Season.objects.get(name=current_season_name)
    all_seasons = Season.objects.all()
    all_memberships = Membership.objects.filter(season=current_season).order_by('-num_wins', 'num_losses', '-num_ties')
    return render_to_response('results.html',
                              {'all_seasons': all_seasons, 'current_season': current_season, 'all_memberships':all_memberships },
                              context_instance=RequestContext(request))
    

def display_season(request, season_name):
    season_name = season_name.strip()
    season = get_object_or_404(Season, slug_name=season_name)
    all_memberships = Membership.objects.filter(season=season).order_by('-num_wins', 'num_losses', '-num_ties')
    
    return render_to_response('results-detailed.html',
                              {'season': season, 'all_memberships':all_memberships},
                              context_instance=RequestContext(request))

def display_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    return render_to_response('game.html',
                              {'game': game},
                              context_instance=RequestContext(request))
