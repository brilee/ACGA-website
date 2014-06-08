from django.template import RequestContext
from django.template.loader import get_template
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from models import Document, Event
from CGL.models import School

def display_members(request):
    all_schools = School.objects.all()
    recent_schools = School.objects.order_by("-id")[:5]
    return render(request, 'members.html', locals())

def display_emails(request):
    all_schools = School.objects.all()

    return render(request, 'all-emails.html', locals())

def display_resources(request):
    public_documents = Document.objects.filter(public=True)

    return render(request, 'resources.html', locals())

def display_upcoming_event(request):
    all_events = Event.objects.all().order_by('-event_date')
    requested_event = Event.objects.get_upcoming_event()
    return render(request, 'events.html', locals())

def display_event(request, event_slug):
    all_events = Event.objects.all().order_by('-event_date')
    requested_event = get_object_or_404(Event, slug_name=event_slug)
    return render(request, 'events.html', locals())
