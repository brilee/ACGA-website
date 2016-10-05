from datetime import date, timedelta
import itertools
import urlparse
from django.conf import settings
from django.core.urlresolvers import reverse

from captain_auth import AUTH_KEY_COOKIE_NAME
from kgs.scrape_games import get_KGS_games, filter_likely_games, download_gamefile
from CGL.models import CurrentSeasons, SCHOOL1, SCHOOL2, Player, Game, Match, Forfeit, Team, School, SchoolAuth
from CGL.matchmaking import best_matchup

def get_actively_participating_schools():
    school_ids = [d['school'] for d in Team.objects.filter(season__in=CurrentSeasons.objects.get()).values("school")]

    return School.objects.filter(id__in=school_ids)

def regenerate_school_auth_keys(school):
    SchoolAuth.objects.filter(school=school).delete()
    auth, created = SchoolAuth.objects.get_or_create(school=school)
    return (school.contact_email,
        urlparse.urlunparse([
            "",
            settings.WEB_URL,
            reverse("captain_dashboard"), "",
            AUTH_KEY_COOKIE_NAME + "=" + auth.secret_key, ""]
    ))

def fetch_match_results(season):
    debug_messages = []
    round = season.round_set.get_previous_round()
    if not round:
        debug_messages.append("No previous round found for %s" % season)
        return debug_messages

    for match in round.match_set.all():
        school1 = match.team1.school
        school2 = match.team2.school
        debug_messages.append("Handling %s vs %s" % (school1.name, school2.name))
        team1_player = Player.objects.get_or_create(name="Unknown Player", school=school1)[0]
        team2_player = Player.objects.get_or_create(name="Unknown Player", school=school2)[0]
        for i in "123":
            existing_game = Game.objects.filter(match=match, board=i)
            if existing_game:
                debug_messages.append("Board %s already exists" % i)
                continue
            forfeit = Forfeit.objects.filter(match=match, board=i)
            if forfeit:
                debug_messages.append("Found forfeit, not going to try downloading match %s" % i)
                continue

            likely_games, messages = fetch_likely_games(match.team1, match.team2, match, i)
            debug_messages.extend(messages)

            if likely_games:
                kgs_game = likely_games[0]
                if kgs_game.white.lower().startswith(school1.KGS_name.lower()):
                    white_school = SCHOOL1
                    white_player = team1_player
                    black_player = team2_player
                else:
                    white_school = SCHOOL2
                    white_player = team2_player
                    black_player = team1_player

                gamefile = download_gamefile(kgs_game.sgf_url)
                g = Game(
                    white_player=white_player,
                    black_player=black_player,
                    match=match,
                    board=i,
                    white_school=white_school,
                    gamefile=gamefile,
                )
                g.save()
            else:
                debug_messages.append("Couldn't find game for %s vs %s board %s" % (school1.name, school2.name, i))
    return debug_messages

def fetch_likely_games(team1, team2, match, board):
    debug_messages = []
    debug_messages.append("Fetching game info from KGS")
    year = match.round.date.year
    month = match.round.date.month

    usernames = []
    for team in (team1, team2):
        if team.team_name.endswith(" B"):
            usernames.append((team.school.KGS_name + str(int(board) + 3)).lower())
        else:
            usernames.append((team.school.KGS_name + board).lower())

    likely_games = []
    for username in usernames:
        debug_messages.append("Trying username %s" % username)
        all_games = get_KGS_games(username, year, month)
        likely_games = filter(
            filter_likely_games(
                usernames, date=match.round.date),
            all_games
        )
        if likely_games:
            break

    return likely_games, debug_messages

def make_round_pairings(season, round):
    debug_messages = []
    all_teams = set(Team.objects.filter(season=season, still_participating=True))
    already_matched = set(itertools.chain(*[(match.team1.id, match.team2.id) for match in round.match_set.all()]))
    teams_with_byes = set(bye.team.id for bye in round.bye_set.all())
    ignore_schools = already_matched | teams_with_byes
    team_pool = [t for t in all_teams if t.id not in ignore_schools]

    if len(team_pool) < 2:
        debug_messages.append("There are fewer than 2 unpaired schools, nothing to do for %s" % season.name)
        return debug_messages

    existing_matchups = Match.objects.filter(round__season=season)

    debug_messages.append("Making matches for %s, round %s on %s" % (season, round.round_number, round.date))
    team_pairings, team_bye = best_matchup(team_pool, existing_matchups)
    for pairing in team_pairings:
        debug_messages.append('%s vs. %s' % pairing)
    if team_bye:
        debug_messages.append('%s has a bye this round' % team_bye)
    debug_messages.append('Registering matchups!')
    for pairing in team_pairings:
        Match.objects.create(round=round, team1=pairing[0], team2=pairing[1])
    return debug_messages

def update_school_activeness():
    School.objects.all().update(inCGL=False)
    seasons = CurrentSeasons.objects.get()
    current_schools = set([school for season in seasons for school in season.schools.all()])
    all_schools = School.objects.all()
    for school in all_schools:
        school.inCGL = school in current_schools
        school.save()

def update_player_record(player):  
    player.num_wins = 0
    player.num_losses = 0

    # Assume player is inactive until evidence to contrary is found
    player.isActive = False

    for game in player.game_set():
        if (date.today() - game.match.round.date) < timedelta(days=180):
            player.isActive = True
        if game.winner == player:
            player.num_wins += 1
        else:
            player.num_losses += 1

    player.save()

def update_match_and_schools(season):
    # reset all scores for this season; recompute from scratch.
    Team.objects.filter(season=season).update(
        num_wins=0,
        num_losses=0,
        num_ties=0,
        num_byes=0,
        num_forfeits=0
    )
        
    # compute the result of each match, based on games and forfeits
    # at the same time, tally up each school's wins/losses
    all_rounds = season.round_set.filter(date__lte=date.today())
    for round in all_rounds:
        for match in round.match_set.all():
            m = match
            
            # Clear previously calculated match record
            m.score1 = 0
            m.score2 = 0

            # Figure out who won the match. Make note of forfeits.
            for game in m.game_set.all():
                if game.winner == game.team1_player:
                    m.score1 += 1
                else:
                    m.score2 += 1
            for forfeit in m.forfeit_set.all():
                if forfeit.team1_noshow and not forfeit.team2_noshow:
                    m.score2 += 1
                elif forfeit.team2_noshow and not forfeit.team1_noshow:
                    m.score1 += 1
            m.save()


            if m.is_exhibition:
                # shortcircuit here. don't want to count exhibition matches
                # towards season results.
                continue

            # Update the school's scores based on match result
            for forfeit in m.forfeit_set.all():
                if forfeit.team1_noshow:
                    m.team1.num_forfeits += 1
                if forfeit.team2_noshow:
                    m.team2.num_forfeits += 1
            if m.score1 > m.score2:
                m.team1.num_wins += 1
                m.team2.num_losses += 1
            elif m.score1 < m.score2:
                m.team1.num_losses += 1
                m.team2.num_wins += 1
            else:
                m.team1.num_ties += 1
                m.team2.num_ties += 1
            m.team1.save()
            m.team2.save()
    # Every team gets a bye for not having played in a round
    # even if they joined the CGL late; this way we can bias
    # newcomers to always getting paired up. By recalculating
    # this value, it's one less source of non-idempotency when
    # creating matchups + byes each round.
    num_rounds = len(all_rounds)
    for team in Team.objects.filter(season=season):
        team.num_byes = num_rounds - team.num_wins - team.num_losses - team.num_ties
        team.save()
