from django.shortcuts import get_object_or_404, render
from django.http import  HttpResponseRedirect

from CGL.forms import CreateGameCommentForm
from CGL.models import School, CurrentSeasons Season, Team, Game, Player, GameComment

def display_schools(request):
    all_schools = School.objects.all()
    recent_schools = School.objects.order_by("-id")[:5]
    return render(request, 'schools.html', locals())

def display_roster(request, school_name):
    school = get_object_or_404(School, slug_name=school_name)
    roster = school.player_set.filter(isActive=1).order_by('rank')
    inactives = school.player_set.filter(isActive=0).order_by('rank')
    participating_seasons = Team.objects.filter(school__slug_name=school_name)

    return render(request, 'roster.html', locals())

def display_current_seasons(request):
    return display_seasons(request, CurrentSeasons.objects.get())
    
def display_seasons(request, seasons):
    if isinstance(seasons, basestring):
        seasons = seasons.strip()
        requested_seasons = [get_object_or_404(Season, slug_name=seasons)]
    elif hasattr(seasons, '__iter__'):
        requested_seasons = seasons

    all_seasons = Season.objects.all()

    return render(request, 'results.html', locals())

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

    return render(request, 'players.html', locals())

def display_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'players-detailed.html', locals())

def display_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    form = CreateGameCommentForm()
    return render(request, 'game-detailed.html', locals())

def submit_comment(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = CreateGameCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            user = request.user
            new_comment = GameComment(game=game, comment=comment, user=user)
            new_comment.save()
    
    return HttpResponseRedirect(game.get_absolute_url())
