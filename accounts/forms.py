from django import forms
from CGL.models import Player, School
from accounts.models import PendingPlayerLinkRequest, SchoolEditPermission

# Damn. I tried to add this, but modelform_factory was only implemented
# in Django 1.5, so I don't get to use it.
#EditPlayerForm = forms.modelform_factory(Player, fields=('name', 'rank', 'KGS_username', 'receiveSpam'))
#EditSchoolForm = forms.modelform_factory(School, fields=('club_president', 'captain', 'contact_email', 'website', 'meeting_info'))
#ApproveLinkRequestForm = forms.modelform_factory(PendingPlayerLinkRequest,
#                           fields=('status',))

class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'rank', 'KGS_username', 'receiveSpam']

class EditSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['club_president', 'captain', 'contact_email', 'website', 'meeting_info']

class ApproveLinkRequestForm(forms.ModelForm):
    '''
    A form that lets a team captain approve a link request
    '''
    class Meta:
        model = PendingPlayerLinkRequest
        fields = ['status']

class PlayerLinkRequestForm(forms.Form):
    '''
    A form that lets users request to link to a player.
    '''
    player = forms.ModelChoiceField(queryset=Player.objects.all())

