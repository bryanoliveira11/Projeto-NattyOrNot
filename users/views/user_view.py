from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from users.forms import LoginForm, RegisterForm


class UserRegisterView(View):
    def get(self, *args, **kwargs):
        # salvando dados na sessão para não perder progresso ao sair da página
        register_data = self.request.session.get('register_data', None)

        form = RegisterForm(register_data)

        # renderiza formulário de registro
        return render(self.request, 'users/pages/register.html', context={
            'form': form,
            'form_action': reverse('users:register'),
            'title': 'Cadastro',
        })

    def post(self, *args, **kwargs):
        POST = self.request.POST
        self.request.session['register_data'] = POST

        form = RegisterForm(POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)  # setando a senha do usuário
            user.save()
            messages.success(
                self.request,
                'Usuário Criado com Sucesso! Por Favor Faça seu Login.'
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

        # renderiza a página de login com get
        return render(self.request, 'users/pages/login.html', context={
            'form': form,
            'form_action': reverse('users:login'),
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
        return render(self.request, 'global/partials/error404.html', context={
            'title': 'Página Não Encontrada',
        })

    # valida se o usuário para logout é o correto
    def post(self, *args, **kwargs):
        if self.request.POST.get('username') != self.request.user.username:  # type:ignore
            messages.error(self.request, 'Usuário de Logout Inválido.')
            return redirect(reverse('users:login'))

        # realiza o logout
        messages.success(self.request, 'Logout Efetuado. Até a Próxima !')
        logout(self.request)
        return redirect(reverse('users:login'))
