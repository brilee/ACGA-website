from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from CGL.models import Player
from accounts.models import PendingPlayerLinkRequest

class EditPlayerForm(forms.ModelForm):
    '''
    A form that lets users update their profile info
    '''
    class Meta:
        model = Player
        fields = ['name', 'rank', 'KGS_username', 'receiveSpam']


class PlayerLinkRequestForm(forms.Form):
    '''
    A form that lets users request to link to a player.
    '''
    player = forms.ModelChoiceField(queryset=Player.objects.all())
