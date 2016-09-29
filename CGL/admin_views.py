from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from CGL.models import School, Player, CurrentSeasons
from CGL.transactional_emails import get_all_email_addresses, render_introductory_email, render_weekly_email, render_reminder_email
from CGL.season_management import make_round_pairings, update_match_and_schools, update_player_record, update_school_activeness, fetch_match_results

@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', locals())

@staff_member_required
def email_dashboard(request):
    schools = School.objects.all()
    emails = get_all_email_addresses()
    weekly_results_email = render_weekly_email()
    weekly_reminder_email = render_reminder_email()
    return render(request, 'email_dashboard.html', locals())

@staff_member_required
def render_introductory_email_view(request, school_id):
    school = School.objects.get(id=int(school_id))
    return HttpResponse(render_introductory_email(school))

@staff_member_required
def round_pairings(request):
    if request.method != 'POST':
        return HttpResponse("Must use POST", status=405)
    debug_messages = []
    seasons = CurrentSeasons.objects.get()
    for season in seasons:
        round = season.round_set.get_next_round()
        if not round:
            debug_messages.append("Couldn't find an upcoming round for %s" % season.name)
            continue
        messages = make_round_pairings(season, round)
        debug_messages.extend(messages)
    return HttpResponse("\n".join(debug_messages))

@staff_member_required
def update_scores(request):
    if request.method != 'POST':
        return HttpResponse("Must use POST", status=405)
    debug_messages = []
    import time; time.sleep(10)
    seasons = CurrentSeasons.objects.get()
    for season in seasons:
        debug_messages.append('Updating %s standings' % (season.name))
        update_match_and_schools(season)
        debug_messages.append('School records updated from match results')
    for player in Player.objects.all():
        update_player_record(player)
    debug_messages.append('All player records updated')
    update_school_activeness()
    debug_messages.append('Updated school inCGL active status')
    return HttpResponse("\n".join(debug_messages))

@staff_member_required
def fetch_results(request):
    if request.method != 'POST':
        return HttpResponse("Must use POST", status=405)
    debug_messages = []
    for season in CurrentSeasons.objects.get():
        messages = fetch_match_results(season)
        debug_messages.extend(messages)
    return HttpResponse("\n".join(debug_messages))

