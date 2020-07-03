from django import forms


class CallbackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите ваше имя',
        'class': 'input input-container__input',
        'id': ''
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите ваш e-mail',
        'class': 'input input-container__input',
        'id': ''
    }))
    text = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Напишите свой вопрос',
        'class': 'textarea',
        'id': ''
    }))
