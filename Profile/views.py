from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Callback
from .forms import CallbackForm


def record_callback(request):
    form = CallbackForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        text = form.cleaned_data.get('text')

        callback = Callback(
            name=name,
            email=email,
            text=text,
        )

        superusers_emails = User.objects.filter(is_superuser=True).values_list('email', flat=True)

        title = "Запрос на обратную связь"
        message = f'Имя: {name}\nПочта: {email}\nВопрос: {text}'

        send_mail(
            title,
            message,
            '"vgforall.ru" <settings.EMAIL_HOST_USER>',
            list(superusers_emails)
        )

        print(title, email)

        callback.save()

        return HttpResponse('success')
    return HttpResponse('invalid')
