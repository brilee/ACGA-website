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
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['collegiatego@gmail.com'],
            )
            return HttpResponseRedirect('/contact/thanks/#form')
        else:
            return render_to_response('contact.html', {'NavID':'contact', 'sidebar':'sidebar3.html', 'form':form})
    else:
        form = ContactForm()
    return render_to_response('contact.html', {'NavID':'contact', 'sidebar':'sidebar3.html', 'form':form})
