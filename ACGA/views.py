from django.template import RequestContext
from django.template.loader import get_template
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import Newsfeed
from CGA.CGL.models import School

def display_home(request):
    latest_posts = Newsfeed.objects.all().order_by('-pub_date')[:3]
    return render_to_response('home.html',
                              {'latest_posts': latest_posts},
                              context_instance=RequestContext(request))

def display_members(request):
    s = School.objects.all()
    recent_schools = School.objects.order_by("-id")[:5]
    return render_to_response('members.html',
                              {'all_schools': s, 'recent_schools': recent_schools},
                              context_instance=RequestContext(request))

def display_school(request, school_name):
    school_name = school_name.strip().replace('_', ' ').replace('-', ' ')
    s = get_object_or_404(School, name=school_name)

    roster = s.player_set.filter(isActive=1).order_by('rank')
    retired = s.player_set.filter(isActive=0)
    
    return render_to_response('member-detailed.html',
                              {'school':s, 'roster':roster, 'retired':retired},
                              context_instance=RequestContext(request))

def display_news(request):
    all_posts = Newsfeed.objects.all().order_by('-pub_date')
    return render_to_response('news.html',
                              {'all_posts': all_posts},
                              context_instance=RequestContext(request))


def display_post(request, post_id):
    post = Newsfeed.objects.get(id=post_id)
    return render_to_response('news-detailed.html',
                              {'post': post},
                              context_instance=RequestContext(request))

def display_emails(request):
    all_schools = School.objects.all()
    return render_to_response('all_emails.html',
                              {'all_schools': all_schools},
                              context_instance=RequestContext(request))

