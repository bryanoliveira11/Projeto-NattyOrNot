from django import forms
from django.utils.html import format_html

from utils.django_forms import add_attr, add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu Usuário')
        add_placeholder(self.fields['password'], 'Digite sua Senha')
        add_attr(self.fields['password'], 'class', 'login-password-field')

    username = forms.CharField(label='Usuário')
    password = forms.CharField(
        label=format_html(
            '<i class="fa-solid fa-lock m-right"></i> Senha'
        ),
        widget=forms.PasswordInput()
    )
