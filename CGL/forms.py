from django import forms
from CGL.models import School, Player

class EditSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['club_president', 'captain', 'contact_email', 'secondary_contacts', 'website', 'meeting_info']

class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'rank', 'KGS_username']
