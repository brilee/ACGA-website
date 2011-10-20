from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=50)
    email = forms.EmailField(required=False, label='Your email')
    message = forms.CharField(widget=forms.Textarea)
