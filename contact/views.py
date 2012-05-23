from django.shortcuts import render_to_response, redirect
from CGA.forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template import RequestContext

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message_and_email = 'Enjoy this message from ' + cd['email'] + ': ' + cd['message']
            send_mail(
                cd['subject'],
                message_and_email,
                'from@example.com',
                ['acga.organizers@gmail.com'],
                fail_silently=False
            )
            return HttpResponseRedirect('/contact/thanks/#form')
        else:
            return render_to_response('contact.html', {'form':form})
    else:
        form = ContactForm()
    return render_to_response('contact.html', {'form':form})
