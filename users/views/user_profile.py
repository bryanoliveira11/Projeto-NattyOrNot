from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from users.forms import ChangePasswordForm, EditForm
from users.models import UserProfile
from utils.get_notifications import get_notifications

User = get_user_model()


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserProfileDetailClassView(View):
    def get_user_profile(self, user_id):
        return UserProfile.objects.filter(user__id=user_id).first()

    def is_google_account_user(self):
        google_account = EmailAddress.objects.filter(
            user_id=self.request.user.id  # type:ignore
        ).first()

        if google_account is not None:
            return True
        return False

    # lançar um alerta na tela de perfil se o email do usuário estiver vázio
    # isso ocorre se a conta for do google e o email já estiver em uso
    def check_email(self):
        user_db = User.objects.filter(pk=self.request.user.pk).first()

        if user_db:
            if not user_db.email:  # type:ignore
                messages.warning(
                    self.request,
                    'Parece que seu Email não está Preenchido. '
                    'Por Favor, Revise seus Dados !'
                )

    def validate_url_user(self, username):
        # 404 em tentativa de editar a url
        if username != self.request.user.username:  # type:ignore
            raise Http404()

    def get_profile_form_action(self):
        return reverse('users:user_profile', args=(self.request.user,))

    def get_password_change_form_action(self):
        return reverse(
            'users:user_profile_change_password', args=(self.request.user,)
        )

    def render_form(
        self, form, form_action, profile_page=False, password_page=False
    ):
        user = self.request.user
        user_profile = self.get_user_profile(user.pk)
        is_google_account = self.is_google_account_user()
        self.check_email()
        notifications, notifications_total = get_notifications(self.request)

        return render(self.request, 'users/pages/user_profile.html', context={
            'user': user,
            'form': form,
            'user_profile': user_profile,
            'notifications': notifications,
            'notification_total': notifications_total,
            'is_google_account': is_google_account,
            'is_profile_page': profile_page,
            'is_change_password_page': password_page,
            'form_action': form_action,
            'title': f'Perfil ({user})',
        })

    # get vai mostrar a foto de perfil do user e seus dados
    def get(self, *args, **kwargs):
        self.validate_url_user(self.kwargs.get('username'))
        form = EditForm(instance=self.request.user)
        return self.render_form(
            form=form,
            profile_page=True,
            form_action=self.get_profile_form_action()
        )

    # post permitirá que o user edite os dados existentes da conta
    def post(self, *args, **kwargs):
        form = EditForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.request.user
        )

        if form.is_valid():
            user = form.save(commit=False)
            user_picture = form.cleaned_data.get('profile_picture')
            user_profile = self.get_user_profile(self.request.user.pk)

            # alterando foto caso haja dados no form
            if user_picture:
                # user já tem profile
                if user_profile:
                    user_profile.profile_picture = user_picture
                    user_profile.save()

            # salvando
            user.save()
            messages.success(
                self.request,
                'Dados Editados com Sucesso !'
            )
            return redirect(
                reverse('users:user_profile', args=(self.request.user,)),
            )

        return self.render_form(
            form=form,
            profile_page=True,
            form_action=self.get_profile_form_action()
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserProfileChangePassword(UserProfileDetailClassView):
    def get(self, *args, **kwargs):
        self.validate_url_user(self.kwargs.get('username'))
        form = ChangePasswordForm(instance=self.request.user)
        return self.render_form(
            form=form,
            password_page=True,
            form_action=self.get_password_change_form_action()
        )

    def post(self, *args, **kwargs):
        form = ChangePasswordForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.request.user
        )

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(
                self.request,
                'Senha Alterada com Sucesso ! Por Favor, Faça seu Login.'
            )

            return redirect(reverse('users:login'))

        return self.render_form(
            form=form,
            password_page=True,
            form_action=self.get_password_change_form_action()
        )
