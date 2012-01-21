from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=50)
    email = forms.EmailField(required=False, label='Your email')
    message = forms.CharField(widget=forms.Textarea)

class ProfileForm(forms.Form):
#    username = forms.CharField(max_length=30, label='Username:', required=False)
#    email = forms.EmailField(max_length=50, label='Email:', required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=300, label='Background - tell us about yourself!', required=False)
    club = forms.CharField(widget=forms.Textarea, max_length=150, label='School/Club affiliation:', required=False)
    handles = forms.CharField(max_length=150, label='KGS/IGS/OGS rankings or usernames', required=False)
    aga = forms.BooleanField(label='AGA Member?', required=False)
