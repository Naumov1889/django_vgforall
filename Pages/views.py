from django.shortcuts import render_to_response, redirect, render
from django.template.context_processors import csrf
from django.contrib import auth
from Profession import settings
from django import forms
from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage

# Create your views here.


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()
    message = forms.CharField()
    copy = forms.BooleanField(required=False)


def home_page(request):
    return render(request, 'HomeExtension.html', {'username': auth.get_user(request).username})


def about_project_page(request):
    return render_to_response('AboutProject.html')


def contact_us(request):
    args = {}
    args.update({"email": auth.get_user(request).email})
    args.update(csrf(request))
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            copy = form.cleaned_data['copy']

            recipients = ["barkovgb@yandex.ru"]  # Адрес, на который приходит почта от пользователей сайта

            if copy:
                recipients.append(sender)
            try:
                msg = EmailMessage(subject, message,
                                   from_email=settings.EMAIL_HOST_USER,
                                   to=recipients,
                                   headers={'From': auth.get_user(request).email})
                msg.content_subtype = 'html'
                msg.send(fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return redirect("/")
    else:
        return render_to_response('ExtensionContactForm.html', args)



def confidentiality_page(request):
    return render(request, 'confidentiality.html')


def terms_page(request):
    return render(request, 'terms.html')

def about_page(request):
    return render(request, 'about.html')

def about_page_2(request):
    return render(request, 'about_2.html')