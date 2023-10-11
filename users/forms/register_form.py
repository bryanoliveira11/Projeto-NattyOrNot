from collections import defaultdict

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from utils.django_forms import add_attr, add_placeholder, strong_password

User = get_user_model()


class PasswordValidation:
    def __init__(self, cleaned_data) -> None:
        self.cleaned_data = cleaned_data
        self._my_errors: defaultdict = defaultdict(list)

    def password_validation(self):
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


class RegisterForm(forms.ModelForm, PasswordValidation):
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
        help_text=(
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.'
        ),
        error_messages={
            'required': 'Digite seu Usuário.',
            'min_length': 'O Usuário deve ter no Mínimo 4 Dígitos.',
            'max_length': 'O Usuário deve ter no Máximo 150 Dígitos.',
        }
    )

    email = forms.EmailField(
        label='E-mail',
        help_text=('E-mail Precisa ser Válido.'),
        error_messages={
            'required': 'Digite seu E-mail.',
        }
    )

    password = forms.CharField(
        label='Senha',
        error_messages={
            'required': 'Digite sua Senha.'
        },
        help_text=(
            'Senha deve ter ao menos uma letra mínuscula, uma letra '
            'maiúscula e um número. Mínimo de 8 dígitos.'
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
        label='Foto de Perfil',
        help_text='* Não Obrigatório',
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
        # validando usuário
        username = self.cleaned_data.get('username')
        username_database = User.objects.filter(
            username__iexact=username
        ).first()

        if username_database:
            self._my_errors['username'].append(
                'Este Usuário Está em Uso.'
            )
        return username

    def clean_email(self):
        # validando se o email já existe no banco
        email = self.cleaned_data.get('email')
        email_database = User.objects.filter(email__iexact=email).first()

        if email_database:
            self._my_errors['email'].append(
                'Este E-mail Está em Uso.'
            )

        return email

    def clean(self, *args, **kwargs):
        self.password_validation()

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
        username = self.cleaned_data.get('username')
        username_database = User.objects.filter(
            username__iexact=username
        ).first()

        # validando se o username existente no banco tem um id diferente da instancia
        if username_database:
            if username_database.pk != self.instance.pk:
                self._my_errors['username'].append(
                    'Este Usuário Está em Uso.'
                )
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_database = User.objects.filter(email__iexact=email).first()

        # validando se o email existente no banco tem um id diferente da instancia
        if email_database:
            if email_database.pk != self.instance.pk:
                self._my_errors['email'].append(
                    'Este E-mail Está em Uso.'
                )
        return email

    def clean(self, *args, **kwargs):
        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean(*args, **kwargs)


class ChangePasswordForm(forms.ModelForm, PasswordValidation):
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
        help_text=(
            'Senha deve ter ao menos uma letra mínuscula, uma letra '
            'maiúscula e um número. Mínimo de 8 dígitos.'
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
        self.password_validation()

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean(*args, **kwargs)
