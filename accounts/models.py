from django.db import models
from django.contrib.auth.models import User
from CGL.models import Player, School

class SchoolEditPermission(models.Model):
    school = models.ForeignKey(School, 
        help_text="Gives permission to edit school and all players, as well as create players.")
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode('%s can edit %s' % (self.user, self.school))

class PendingPlayerLinkRequest(models.Model):
    user = models.ForeignKey(User)
    player = models.ForeignKey(Player)
    rejected = models.BooleanField(default=False)

    @models.permalink
    def get_absolute_url(self):
        return ('accounts.views.display_link_request', [str(self.id)])

    def __unicode__(self):
        return unicode('REJECTED' if self.rejected else '') +\
            unicode('%s requests %s' % (self.user, self.player))