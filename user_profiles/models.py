from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    description = models.TextField(null=True, blank=True)
    club = models.CharField(max_length=150, null=True, blank=True)
    handles = models.CharField(max_length=150, null=True, blank=True)
    aga = models.BooleanField()
    
    def __unicode__(self):
       return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
        if created:
            print('creating user profile through models')
            UserProfile.objects.create(user=instance)
            
post_save.connect(create_user_profile, sender=User, dispatch_uid="CGA.user_profiles.models")

#class Club(models.Model):
#    name = models.CharField(max_length=100)
#    description = models.TextField()
#    rep = models.CharField(max_length=50)
#    members = models.TextField()
#    aga = models.BooleanField()
    
#    def __unicode__(self):
#        return self.name
