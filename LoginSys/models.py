from django.db import models
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.


class RegistrationForm(UserCreationForm):  # Переопределение формы регистрации
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email",)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Формат номера: '+79999999999'. До 15 цифр.")

    # Атрибуты
    email = models.EmailField()
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # Функции
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfessionalRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(ProfessionalRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs['class'] = 'input input-container__input'
        self.fields['username'].widget.attrs['placeholder'] = 'Введите логин'
        self.fields['password1'].help_text = ''
        self.fields['password1'].widget.attrs['class'] = 'input input-container__input'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs['class'] = 'input input-container__input'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        self.fields['email'].help_text = ''
        self.fields['email'].widget.attrs['class'] = 'input input-container__input'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите email'
        self.fields['email'].required = 'required'

    def clean(self):
        cleaned_data = super().clean()

        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', 'Пользователь с такой почтой уже существует. Попробуйте <a style="color:#be1622" data-popbox-close="popbox-register" data-popbox-target="popbox-password-recovery">восстановить пароль</a>, если вы его забыли')

        return cleaned_data





class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "Пользователь с таким e-mail не зарегистрирован."
            self.add_error('email', msg)
        return email