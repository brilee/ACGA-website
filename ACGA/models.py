from django.db import models
import os
import datetime


class Newsfeed(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100, help_text = 'This text appears in the recent announcements on the sidebar')
    preview = models.TextField(help_text = 'The first few sentences of the post')
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def get_date(self):
        return unicode(self.pub_date.strftime('%Y-%B-%d'))
    
    def __unicode__(self):
        return unicode('%s published on %s' % (self.title, self.pub_date.strftime('%Y-%B-%d')))

class Document(models.Model):
    def upload_location(instance, filename):
        return os.path.join('Documents', filename)
    
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, help_text='A brief summary of the document')
    author = models.CharField(max_length=50)
    upload = models.FileField(upload_to=upload_location, help_text='Upload file here. PDF strongly preferred.')
    uploaded = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False, help_text='Should this document be accessible by anyone?')

    def __unicode__(self):
        return unicode('%s by %s' %(self.title, self.author))

class EventManager(models.Manager):
    def get_upcoming_event(self):
        upcoming_event = super(EventManager, self).filter(event_date__gte=datetime.datetime.now()
                                ).order_by('event_date')
        if upcoming_event:
            return upcoming_event[0]
        else:
            return super(EventManager, self).none()
        
class Event(models.Model):
    title = models.CharField(max_length=100)
    slug_name = models.SlugField()
    event_description = models.TextField(blank=True)
    event_date = models.DateField()
    objects = EventManager()

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('CGA.ACGA.views.display_event', [str(self.slug_name)]) 
