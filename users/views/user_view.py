from os import environ

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from users.email_service import send_html_mail
from users.forms import (ChangePasswordForm, ForgotPassword, LoginForm,
                         RegisterForm)
from users.models import UserProfile
from users.templates.emails.email_templates import \
    forgot_password_email_template
from utils.get_notifications import get_notifications
from utils.get_profile_picture import get_profile_picture
from utils.strings import generate_random_code

User = get_user_model()

EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', '')


class UserRegisterView(View):
    def get(self, *args, **kwargs):
        # salvando dados na sessão para não perder progresso ao sair da página
        register_data = self.request.session.get('register_data', None)

        form = RegisterForm(register_data)

        notifications, notifications_total = get_notifications(self.request)

        # renderiza formulário de registro
        return render(self.request, 'users/pages/register.html', context={
            'form': form,
            'form_action': reverse('users:register'),
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': 'Cadastro',
            'is_register_page': True,
        })

    def post(self, *args, **kwargs):
        POST = self.request.POST
        self.request.session['register_data'] = POST

        form = RegisterForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)  # setando a senha do usuário
            user.save()  # criando usuário no banco

            # pegando a foto de perfil que o usuário enviou
            user_picture = form.cleaned_data.get('profile_picture', '')
            # criando perfil mesmo se não houver imagem
            UserProfile.objects.create(
                user=user,
                profile_picture=user_picture
            )

            messages.success(
                self.request,
                'Usuário Criado com Sucesso ! Por Favor Faça seu Login.'
            )
            # deletando dados salvos na sessão
            del (self.request.session['register_data'])

            # redireciona para o login em caso de sucesso
            return redirect(reverse('users:login'))

        # redireciona para a página de registro se houver erros no form
        return redirect(reverse('users:register'))


class UserLoginView(View):
    def get(self, *args, **kwargs):
        form = LoginForm()

        notifications, notifications_total = get_notifications(self.request)

        # renderiza a página de login com get
        return render(self.request, 'users/pages/login.html', context={
            'form': form,
            'form_action': reverse('users:login'),
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': 'Login',
            'is_login_page': True,
        })

    def post(self, *args, **kwargs):
        POST = self.request.POST
        form = LoginForm(POST)

        # valida se o formulário é válido e tenta autenticar o user pelo banco
        if form.is_valid():
            authenticated_user = authenticate(
                request=self.request,
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', '')
            )

            # login com sucesso
            if authenticated_user is not None:
                login(self.request, user=authenticated_user)
                get_profile_picture(self.request, authenticated_user)
                messages.success(
                    self.request,
                    f'Login Efetuado com Sucesso na Conta {self.request.user}.'
                )
                return redirect(reverse('users:user_dashboard'))
            # errou as credenciais
            else:
                messages.error(self.request, 'Credenciais Inválidas.')
        # deixou os campos vázios
        else:
            messages.error(self.request, 'Usuário ou Senha Inválidos.')

        return redirect(reverse('users:login'))


class UserLogoutView(View):
    # vai levantar erro se o usuário fizer get ao invés de post
    def get(self, *args, **kwargs):
        raise Http404()

    # valida se o usuário para logout é o correto
    def post(self, *args, **kwargs):
        user = self.request.user.get_username()

        if self.request.POST.get('username') != user:
            messages.error(self.request, 'Usuário de Logout Inválido.')
            return redirect(reverse('users:login'))

        # realiza o logout
        messages.success(self.request, 'Logout Efetuado. Até a Próxima !')

        if self.request.session.get('user_picture'):
            del self.request.session['user_picture']

        logout(self.request)
        return redirect(reverse('users:login'))


class UserForgotPasswordBase(View):
    def save_code(self, user, code: str):
        user_profile = UserProfile.objects.filter(user=user).first()

        if not user_profile:
            return

        user_profile.forgot_password_code = code
        user_profile.save()

        self.request.session['reset_password'] = {
            'user_id': user_profile.user.pk,
        }
        self.request.session.save()

    def send_code_email(self, user_email: str, code: str):
        send_mail(
            'Reset de Senha - NattyOrNot',
            'Recebemos seu Pedido de Reset de Senha, seu código é '
            f'{code}. '
            'Informe os 6 digitos no local correto para continuar.',
            environ.get('EMAIL_HOST_USER', ''),
            [user_email],
        )

    def render_form(
        self, form, form_action: str,
        is_forgot_pass_page=True,
        page='email-page',
    ):
        notifications, notifications_total = get_notifications(self.request)

        return render(
            self.request, 'users/pages/forgot_password.html', context={
                'form': form,
                'form_action': form_action,
                'notifications': notifications,
                'notification_total': notifications_total,
                'title': 'Esqueci Minha Senha',
                'is_forgot_password_page': is_forgot_pass_page,
                'pageAttr': page,
            }
        )

    def is_user_authenticated(self):
        if self.request.user.is_authenticated:
            return True
        return False


class UserForgotPasswordView(UserForgotPasswordBase):
    def get(self, *args, **kwargs):
        if self.is_user_authenticated():
            return redirect(reverse('training:home'))

        form = ForgotPassword(is_email=True)

        return self.render_form(
            form=form,
            form_action=reverse('users:forgot_password_email'),
        )

    def post(self, *args, **kwargs):
        form = ForgotPassword(
            True,
            False,
            self.request.POST
        )

        if form.is_valid():
            cleaned_data = form.cleaned_data.get('cleaned_data')
            user_email = cleaned_data.get(
                'email'
            ) if cleaned_data is not None else ''

            user = form.cleaned_data.get('user')
            code = generate_random_code()

            # mandando email
            send_html_mail(
                subject='Reset de Senha - NattyOrNot',
                html_content=forgot_password_email_template(code),
                sender=EMAIL_HOST_USER,
                recipient_list=[user_email],
                dev_mode=False,
            )

            self.save_code(user, code)
            messages.warning(
                self.request,
                'Enviamos um código de 6 dígitos para seu E-mail. '
                'Por favor, informe o código no campo abaixo para continuar.'
            )
            return self.render_form(
                form=ForgotPassword(is_code=True),
                form_action=reverse('users:forgot_password_code'),
                page='code-page',
            )

        return self.render_form(
            form=form,
            form_action=reverse('users:forgot_password_email'),
        )


class UserForgotPasswordValidateCode(UserForgotPasswordBase):
    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        form = ForgotPassword(
            False,
            True,
            self.request.POST
        )

        if form.is_valid():
            cleaned_data = form.cleaned_data.get('cleaned_data')
            code = cleaned_data.get('code') if cleaned_data is not None else ''

            user_data = self.request.session.get('reset_password')
            user_id = user_data.get('user_id') if user_data is not None else ''

            user_profile = UserProfile.objects.filter(
                user=user_id,
            ).first()

            if user_profile and code == user_profile.forgot_password_code:
                form = ChangePasswordForm()

                return self.render_form(
                    form=form,
                    form_action=reverse(
                        'users:forgot_password_change_password'
                    ),
                    is_forgot_pass_page=False,
                    page='reset-page',
                )

        messages.error(self.request, 'Código Inválido.')
        return self.render_form(
            form=form,
            form_action=reverse('users:forgot_password_code'),
            page='code-page',
        )


class UserForgotPasswordReset(UserForgotPasswordBase):
    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        user = User.objects.filter(
            pk=self.request.session['reset_password'].get(
                'user_id'
            )
        ).first()

        form = ChangePasswordForm(
            data=self.request.POST or None,
            instance=user
        )

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(
                self.request,
                'Senha Alterada com Sucesso ! Por Favor, Faça seu Login.'
            )
            del self.request.session['reset_password']
            return redirect(reverse('users:login'))

        return self.render_form(
            form=form,
            form_action=reverse(
                'users:forgot_password_change_password'
            ),
            page='reset-page'
        )
