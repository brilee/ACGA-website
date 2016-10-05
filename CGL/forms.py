from django import forms
from CGL.models import School, Player, Team, MAX_PLAYERS_PER_ROSTER

class EditSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['club_president', 'captain', 'contact_email', 'secondary_contacts', 'website', 'meeting_info']

class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'rank', 'KGS_username']

class EditTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['players']
        widgets = {
            'players': forms.CheckboxSelectMultiple()
        }

    def clean_players(self):
        data = self.cleaned_data['players']
        if len(data) > MAX_PLAYERS_PER_ROSTER:
            raise forms.ValidationError("You cannot have more than %s players on your team" % MAX_PLAYERS_PER_ROSTER)
        return data