from django.template import RequestContext
from django.template.loader import get_template
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from models import Newsfeed, Document
from CGA.CGL.models import School

def display_home(request):
    latest_posts = Newsfeed.objects.all().order_by('-pub_date')[:3]

    return direct_to_template(request, 'home.html', locals())

def display_members(request):
    all_schools = School.objects.all()
    recent_schools = School.objects.order_by("-id")[:5]
    return direct_to_template(request, 'members.html', locals())

def display_news(request):
    all_posts = Newsfeed.objects.all().order_by('-pub_date')

    return direct_to_template(request, 'news.html', locals())

def display_post(request, post_id):
    post = Newsfeed.objects.get(id=post_id)

    return direct_to_template(request, 'news-detailed.html', locals())

def display_emails(request):
    all_schools = School.objects.all()

    return direct_to_template(request, 'all-emails.html', locals())

def display_resources(request):
    public_documents = Document.objects.filter(public=True)

    return direct_to_template(request, 'resources.html', locals())
