from django.views.generic.simple import direct_to_template
from forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

def contact(request, template='contact.html', redirect='contact/thanks/#form'):
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
            return HttpResponseRedirect(redirect)
        else:
            return direct_to_template(request, 'contact.html', locals())
    else:
        if request.user.is_authenticated():
            form = ContactForm(initial={'email': request.user.email})
        else:
            form = ContactForm()

    return direct_to_template(request, 'contact.html', locals())

def join_CGL(request):
    return contact(request, template='join_CGL.html', redirect='/CGL/join/thanks/#form')
    
