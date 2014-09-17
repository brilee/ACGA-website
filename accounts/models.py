from django.db import models
from django.contrib.auth.models import User
from CGL.models import Player, School, Match, Game, Forfeit

class SchoolEditPermissionManager(models.Manager):
    def get_all_schools(self, user):
        return [perm.school for perm in self.filter(user=user)]

    def has_edit_permissions(self, user, obj):
        schoolperms = self.get_all_schools(user)
        if type(obj) == Player:
            return obj.school in schoolperms
        elif type(obj) == School:
            return obj in schoolperms
        elif type(obj) == Match:
            return obj.team1.school in schoolperms or obj.team2.school in schoolperms
        elif type(obj) == Game:
            return obj.match.team1.school in schoolperms or obj.match.team2.school in schoolperms
        elif type(obj) == Forfeit:
            return obj.match.team1.school in schoolperms or obj.match.team2.school in schoolperms
        elif type(obj) == PendingPlayerLinkRequest:
            return obj.player.school in schoolperms
        else:
            return False

class SchoolEditPermission(models.Model):
    school = models.ForeignKey(School, 
        help_text="Gives permission to edit school and all players, as well as create players.")
    user = models.ForeignKey(User)
    objects = SchoolEditPermissionManager()

    def __unicode__(self):
        return u'{} can edit {}'.format(self.user, self.school)

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
        return ('accounts.views.edit_link_request', [str(self.id)])

    def __unicode__(self):
        return u'{} - {} requests {}'.format(self.status, self.user.username, self.player.name)

    def save(self, *args, **kwargs):
        super(PendingPlayerLinkRequest, self).save(*args, **kwargs)
        if self.status == 'Approved':
            self.player.user = self.user
            self.player.save()
        elif self.status == 'Rejected' and self.player.user == self.user:
            self.player.user = None
            self.player.save()



