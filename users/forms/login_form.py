from django import forms

from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu Usuário')
        add_placeholder(self.fields['password'], 'Digite sua Senha')

    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
