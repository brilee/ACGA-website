from django import forms
from CGL.models import Player, School, Game, Forfeit
from accounts.models import PendingPlayerLinkRequest, SchoolEditPermission
from django.contrib.auth.models import User

# Damn. I tried to add this, but modelform_factory was only implemented
# in Django 1.5, so I don't get to use it.
#EditPlayerForm = forms.modelform_factory(Player, fields=('name', 'rank', 'KGS_username', 'receiveSpam'))
#EditSchoolForm = forms.modelform_factory(School, fields=('club_president', 'captain', 'contact_email', 'website', 'meeting_info'))
#ApproveLinkRequestForm = forms.modelform_factory(PendingPlayerLinkRequest,
#                           fields=('status',))

class UsernameReminderForm(forms.Form):
    email = forms.EmailField(max_length=254, label="Email address")
    def save(self):
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        email = self.cleaned_data['email']
        users = User.objects.filter(email__iexact=email)
        for user in users:
            subject = 'Username reminder for email %s' % email
            body = render_to_string('username_reminder.txt', locals())
            send_mail(subject, body, 'ACGA.organizers@gmail.com', [user.email]) 
        
class EditPlayerForm(forms.ModelForm):
    '''
    A form that lets team captains / players edit or create a player
    For creating players, the school is implicitly derived
    from the URL hierarchy.
    '''
    class Meta:
        model = Player
        fields = ['name', 'rank', 'KGS_username', 'receiveSpam']

class EditSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['club_president', 'captain', 'contact_email', 'website', 'meeting_info']

class EditGameForm(forms.ModelForm):
    '''
    A form that lets team captains edit or create a game record
    For creating game records, the match is implicitly derived from
    the URL hierarchy.
    '''
    class Meta:
        model = Game
        fields = ['board', 'gamefile', 'white_school', 'winning_school', 'school1_player', 'school2_player']


class EditForfeitForm(forms.ModelForm):
    '''
    A form that lets team captains edit or create a forfeit
    For creating forfeits, the match is implicitly derived from
    the URL hierarchy.
    '''
    class Meta:
        model = Forfeit
        fields = ['board', 'school1_noshow', 'school2_noshow']


class EditLinkRequestForm(forms.ModelForm):
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
