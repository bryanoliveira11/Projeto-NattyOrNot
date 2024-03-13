from collections import defaultdict

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from utils.django_forms import add_placeholder, strong_password

User = get_user_model()


class ValidateFields:
    def __init__(self, cleaned_data) -> None:
        self.cleaned_data = cleaned_data
        self._my_errors: defaultdict = defaultdict(list)

    def validate_password(self):
        # validando se as senhas batem
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            self._my_errors['password'].append(
                'Senhas Precisam ser Iguais.'
            )
            self._my_errors['password2'].append(
                'Senhas Precisam ser Iguais.'
            )

    def validate_username(
        self, is_register=False, is_edit=False, instance=None
    ):
        # validando usuário
        username = self.cleaned_data.get('username')
        username_database = User.objects.filter(
            username__iexact=username
        ).first()

        if not username_database:
            return username

        if is_register:
            self._my_errors['username'].append(
                'Este Usuário Está em Uso.'
            )
            return username

        if is_edit and instance:
            if username_database.pk != instance.pk:
                self._my_errors['username'].append(
                    'Este Usuário Está em Uso.'
                )
            return username

    def validate_email(self, is_register=False, is_edit=False, instance=None):
        # validando se o email já existe no banco
        email = self.cleaned_data.get('email')
        email_database = User.objects.filter(email__iexact=email).first()

        if not email_database:
            return email

        if is_register:
            if email_database:
                self._my_errors['email'].append(
                    'Este E-mail Está em Uso.'
                )
            return email

        if is_edit and instance:
            if email_database.pk != instance.pk:
                self._my_errors['email'].append(
                    'Este E-mail Está em Uso.'
                )
            return email


class RegisterForm(forms.ModelForm, ValidateFields):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_placeholder(self.fields['username'], 'Digite seu Usuário')
        add_placeholder(self.fields['first_name'], 'Digite seu Nome')
        add_placeholder(self.fields['last_name'], 'Digite seu Sobrenome')
        add_placeholder(self.fields['email'], 'EX.: email@dominio.com')
        add_placeholder(self.fields['password'], 'Digite sua Senha')
        add_placeholder(self.fields['password2'], 'Confirme sua Senha')

    first_name = forms.CharField(
        label='Nome', max_length=150,
        error_messages={
            'required': 'Digite seu Nome.',
            'max_length': 'O Nome deve ter no Máximo 150 Dígitos.',
        }
    )

    last_name = forms.CharField(
        label='Sobrenome', max_length=150,
        error_messages={
            'required': 'Digite seu Sobrenome.',
            'max_length': 'O Sobrenome deve ter no Máximo 150 Dígitos.',
        }
    )

    username = forms.CharField(
        label='Usuário', min_length=4, max_length=150,
        help_text=format_html(
            '''
          <p class="helptext-p">&#x2022; Mínimo de 4 Dígitos</p>
          <p class="helptext-p">&#x2022; Letras</p>
          <p class="helptext-p">&#x2022; Números</p>
          <p class="helptext-p">&#x2022; @/./+/-/_</p>
            '''
        ),
        error_messages={
            'required': 'Digite seu Usuário.',
            'min_length': 'O Usuário deve ter no Mínimo 4 Dígitos.',
            'max_length': 'O Usuário deve ter no Máximo 150 Dígitos.',
        }
    )

    email = forms.EmailField(
        label=format_html(
            '<i class="fa-solid fa-envelope m-right"></i> E-mail'
        ),
        help_text=('E-mail Precisa ser Válido.'),
        error_messages={
            'required': 'Digite seu E-mail.',
        }
    )

    password = forms.CharField(
        label=format_html(
            '<i class="fa-solid fa-lock m-right"></i> Senha'
        ),
        error_messages={
            'required': 'Digite sua Senha.'
        },
        help_text=format_html(
            '''
          <p class="helptext-p">&#x2022; Mínimo de 8 Dígitos</p>
          <p class="helptext-p">&#x2022; 1x Letra Maiúscula</p>
          <p class="helptext-p">&#x2022; 1x Letra Mínuscula</p>
          <p class="helptext-p">&#x2022; 1x Número</p>
            '''
        ),
        widget=forms.PasswordInput(),
        validators=[strong_password],
    )

    password2 = forms.CharField(
        label='Confirmação de Senha',
        error_messages={
            'required': 'Confirme sua Senha.'
        },
        help_text=(
            'Confirme sua Senha.'
        ),
        widget=forms.PasswordInput()
    )

    profile_picture = forms.FileField(
        label='Foto de Perfil (Opcional)',
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'span-2',
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_username(self):
        return self.validate_username(is_register=True)

    def clean_email(self):
        return self.validate_email(is_register=True)

    def clean(self, *args, **kwargs):
        self.validate_password()

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean(*args, **kwargs)


# este form vai ser usado para editar os dados do usuário
class EditForm(RegisterForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(
        attrs={'class': 'invisible'}
    ))

    password2 = forms.CharField(required=False, widget=forms.PasswordInput(
        attrs={'class': 'invisible'}
    ))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def clean_username(self):
        return self.validate_username(is_edit=True, instance=self.instance)

    def clean_email(self):
        return self.validate_email(is_edit=True, instance=self.instance)

    def clean(self, *args, **kwargs):
        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean(*args, **kwargs)


class ChangePasswordForm(forms.ModelForm, ValidateFields):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_placeholder(self.fields['password'], 'Digite sua Senha')
        add_placeholder(self.fields['password2'], 'Confirme sua Senha')

    password = forms.CharField(
        label='Senha',
        error_messages={
            'required': 'Digite sua Senha.'
        },
        help_text=format_html(
            '''
          <p class="helptext-p">&#x2022; Mínimo de 8 Dígitos</p>
          <p class="helptext-p">&#x2022; 1x Letra Maiúscula</p>
          <p class="helptext-p">&#x2022; 1x Letra Mínuscula</p>
          <p class="helptext-p">&#x2022; 1x Número</p>
            '''
        ),
        widget=forms.PasswordInput(),
        validators=[strong_password],
    )

    password2 = forms.CharField(
        label='Confirmação de Senha',
        error_messages={
            'required': 'Confirme sua Senha.'
        },
        help_text=(
            'Confirme sua Senha.'
        ),
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['password']

    def clean(self, *args, **kwargs):
        self.validate_password()

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean(*args, **kwargs)
