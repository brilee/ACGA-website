from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    description = models.TextField()
    club = models.CharField(max_length=100)
    handles = models.CharField(max_length=100)
    aga = models.BooleanField()
    
    def __unicode__(self):
       return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
            
post_save.connect(create_user_profile, sender=User)

#class Club(models.Model):
#    name = models.CharField(max_length=100)
#    description = models.TextField()
#    rep = models.CharField(max_length=50)
#    members = models.TextField()
#    aga = models.BooleanField()
    
#    def __unicode__(self):
#        return self.name
