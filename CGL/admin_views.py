from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from CGL.models import School
from CGL.transactional_emails import get_all_email_addresses, render_introductory_email, render_weekly_email, render_reminder_email

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
