from django.db import models

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

