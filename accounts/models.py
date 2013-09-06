from django.db import models
from django.contrib.auth.models import User
from CGL.models import Player, School

class SchoolEditPermissionManager(models.Manager):
    def get_all_schools(self, user):
        return [perm.school for perm in super(SchoolEditPermissionManager, 
            self).get_query_set().filter(user=user)]

    def has_edit_permissions(self, user, player):
        return player.school in self.get_all_schools(user)

class SchoolEditPermission(models.Model):
    school = models.ForeignKey(School, 
        help_text="Gives permission to edit school and all players, as well as create players.")
    user = models.ForeignKey(User)
    objects = SchoolEditPermissionManager()

    def __unicode__(self):
        return unicode('%s can edit %s' % (self.user, self.school))

class PendingPlayerLinkRequest(models.Model):
    STATUS_CHOICES = (('Approved', 'Approved'),
                      ('Rejected', 'Rejected'),
                      ('Pending', 'Pending'))
    user = models.ForeignKey(User)
    player = models.ForeignKey(Player)
    status = models.CharField(choices=STATUS_CHOICES, 
                              default='Pending',
                              max_length=8)

    @models.permalink
    def get_absolute_url(self):
        return ('accounts.views.display_link_request', [str(self.id)])

    def __unicode__(self):
        return unicode('%s - %s requests %s' % (self.status, self.user, self.player))

    def save(self, *args, **kwargs):
        super(PendingPlayerLinkRequest, self).save(*args, **kwargs)
        if self.status == 'Approved':
            self.player.user = self.user
            self.player.save()
        elif self.status == 'Rejected' and self.player.user == self.user:
            self.player.user = None
            self.player.save()



