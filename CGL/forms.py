from django import forms
from CGL.models import GameComment, LadderGameComment


class CreateGameCommentForm(forms.ModelForm):
    class Meta:
        model = GameComment
        fields = ['comment']

class CreateLadderGameCommentForm(forms.ModelForm):
    class Meta:
        model = LadderGameComment
        fields = ['comment']
