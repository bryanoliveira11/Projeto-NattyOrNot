from collections import defaultdict
from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from utils.django_forms import add_attr, add_placeholder

User = get_user_model()


class ForgotPassword(forms.Form):
    def __init__(self, is_email=False, is_code=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        self.is_email = is_email
        self.is_code = is_code

        if is_email:
            self.fields['email'] = forms.EmailField(
                label=format_html(
                    '<i class="fa-solid fa-envelope m-right"></i> E-mail'
                ),
                help_text='E-mail da Conta que quer Acessar.',
                error_messages={'required': 'Digite seu E-mail.'}
            )
            add_placeholder(self.fields['email'], 'EX.: email@dominio.com')
            add_attr(self.fields['email'], 'class', 'span-2')

        if is_code:
            self.fields['code'] = forms.CharField(
                label='Código de Verificação',
                help_text='Enviamos o Código no seu E-mail',
                min_length=6,
                max_length=6
            )
            add_placeholder(self.fields['code'], 'Digite o Código')
            add_attr(self.fields['code'], 'class', 'span-2')

    def clean(self, *args, **kwargs) -> dict[str, Any]:
        cleaned_data = super().clean(*args, **kwargs)
        email_database = None

        if self.is_email:
            email = cleaned_data.get('email')
            email_database = User.objects.filter(email__iexact=email).first()

            if not email_database:
                self._my_errors['email'].append(
                    'Não foi Possível Encontrar este E-mail.'
                )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return {
            'cleaned_data': cleaned_data,
            'user': email_database
        }
