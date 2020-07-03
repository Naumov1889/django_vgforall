# -*- coding utf-8 -*-
from django.http import JsonResponse
from django.contrib import auth
from django.shortcuts import render_to_response, redirect, render
from django.template.context_processors import csrf
from LoginSys.models import ProfessionalRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMessage
from Profession import settings
from django.contrib.auth.models import User
from Profile.models import Profile
import random
import string


# Create your views here.


def login(request):
    args = {}

    if request.is_ajax():
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            try:
                user = auth.authenticate(username=username, password=password)
            except:
                user = None

            if user is not None:
                auth.login(request, user)
                return JsonResponse({'success': 'ok'})
            else:
                return JsonResponse({'success': 'noo'})
        else:
            return JsonResponse({'errors': form.errors})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect("/")


def generate_string(size=24, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# def password_recovery(request):
#     args = {}
#     if request.POST:
#         email = request.POST.get('email', '')
#
#         user = User.objects.filter(email=email).first()
#         print(user)
#
#         if user is not None:
#             user_password = user.password
#             print(user_password)
#
#             subject = "Восстановление пароля"
#             message = "Ваш пароль " + user_password
#             recipients = [email]
#             msg = EmailMessage(subject, message,
#                                from_email=settings.EMAIL_HOST_USER,
#                                to=recipients, )
#             msg.content_subtype = 'html'
#             msg.send(fail_silently=True)
#
#             return redirect("/")
#         else:
#             return False
#
#     else:
#         return render(request, 'login.html')


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, '<span style="color:#28a745;margin: 0 0 1rem 0;">Пароль успешно изменён!</span>',
                             extra_tags='change_password_messages')
            return redirect('personal_info')
        else:
            messages.error(request,
                           '<span style="color:#dc3545;margin: 0 auto 0.25rem 0;">Пожалуйста, исправьте следующие ошибки:</span>',
                           extra_tags='change_password_messages')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ChangeData.html', {
        'form': form
    })


from django.conf import settings as project_settings
from django.core.mail import send_mail

def send_verification_message(username, email):
    title = "Подтверждение регистрации"
    salt = generate_string(24)
    verification_link = "http://127.0.0.1:8000/activate_user/" + username + "/" + salt
    message = "Вы зарегестрировались на сайте vgforall.ru, для завершения регистрации перейдите по ссылке: " + verification_link
    message += "\n\nВаш логин: " + username

    recipients = [email]

    send_mail(
        title,
        message,
        '"vgforall.ru" <project_settings.EMAIL_HOST_USER>',
        recipients
    )

    return salt


# def registration(request):
#     args = {}
#
#     if request.POST:
#         username = request.POST.get('username', '')
#         password1 = request.POST.get('password1', '')
#         password2 = request.POST.get('password2', '')
#         email = request.POST.get('email', '')
#         print(username, password1, password2, email)
#
#         new_user = auth.authenticate(username=username,
#                                      password=password2,
#                                      email=email,)
#         salt = send_verification_message(new_user.username, new_user.email)
#         new_user.profile.activation_salt = salt
#         new_user.is_active = False
#         new_user.save()
#         auth.login(request, new_user)
#         return render(request, 'AccountActivation.html')
#
#     return render(request, 'registration.html', args)

def registration(request):
    args = {}
    args.update(csrf(request))
    args['user_creation_form'] = ProfessionalRegistrationForm()
    # if request.POST:
    #     new_user_form = ProfessionalRegistrationForm(request.POST)
    #     if new_user_form.is_valid():
    #         new_user_form.save()
    #         new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
    #                                      password=new_user_form.cleaned_data['password2'],
    #                                      email=new_user_form.cleaned_data['email'], )
    #         salt = send_verification_message(new_user.username, new_user.email)
    #         new_user.profile.activation_salt = salt
    #         new_user.is_active = False
    #         new_user.save()
    #         auth.login(request, new_user)
    #         return render_to_response('AccountActivation.html')
    #     else:
    #         args['user_creation_form'] = new_user_form


    if request.is_ajax():
        form = ProfessionalRegistrationForm(request.POST)
        if form.is_valid():
            # data = {
            #     'name': form.cleaned_data['name'],
            #     'phone': form.cleaned_data['phone'],
            #     'email': form.cleaned_data['email'],
            #     'message': form.cleaned_data['message']
            # }
            form.save()
            new_user = auth.authenticate(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password2'],
                                         email=form.cleaned_data['email'], )
            salt = send_verification_message(new_user.username, new_user.email)
            new_user.profile.activation_salt = salt
            new_user.is_active = False
            new_user.save()
            auth.login(request, new_user)

            return JsonResponse({'success': 'ok'})
        else:
            return JsonResponse({'errors': form.errors})


    return render_to_response('registration.html', args)



def personal_account(request):
    return render_to_response("../PersonalAccount/templates/PersonalAccount.html")


def personal_tests(request):
    return render_to_response("../PersonalAccount/templates/PersonalTests.html")


from django.contrib.auth.views import PasswordResetView
from LoginSys.models import EmailValidationOnForgotPassword

class MyPasswordResetView(PasswordResetView):
    from_email = '"vgforall.ru" <settings.EMAIL_HOST_USER>'
    form_class = EmailValidationOnForgotPassword

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)

        if self.request.is_ajax():
            return JsonResponse({'success': 'ok'})

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'errors': form.errors})