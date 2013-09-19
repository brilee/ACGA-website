from django import forms
from CGL.models import GameComment


class CreateGameCommentForm(forms.ModelForm):
    class Meta:
        model = GameComment
        fields = ['comment']

