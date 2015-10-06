from django import forms
from CGL.models import GameComment, Player, School

class CreateGameCommentForm(forms.ModelForm):
    class Meta:
        model = GameComment
        fields = ['comment']

class SubmitRosterInformationForm(forms.Form):
    player_name1 = forms.CharField(label="Board 1 player", max_length=100)
    player_is_new1 = forms.BooleanField(label="New player?", initial=False, required=False)
    player_name2 = forms.CharField(label="Board 2 player", max_length=100)
    player_is_new2 = forms.BooleanField(label="New player?", initial=False, required=False)
    player_name3 = forms.CharField(label="Board 3 player", max_length=100)
    player_is_new3 = forms.BooleanField(label="New player?", initial=False, required=False)

    school_name = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(SubmitRosterInformationForm, self).clean()
        school = School.objects.get(name=cleaned_data["school_name"])
        for i in "123":
            player_name = cleaned_data["player_name"+i]
            player_is_new = cleaned_data["player_is_new"+i]
            if not player_is_new and Player.objects.filter(name=player_name, school=school).count() == 0:
                raise forms.ValidationError("Couldn't find player {}".format(player_name))
        return cleaned_data
