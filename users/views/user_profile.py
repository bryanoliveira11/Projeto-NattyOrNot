from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from users.forms import EditForm
from users.models import UserProfile

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

    def render_form(self, form):
        user = self.request.user
        user_profile = self.get_user_profile(user.pk)
        is_google_account = self.is_google_account_user()

        return render(self.request, 'users/pages/user_profile.html', context={
            'user': user,
            'form': form,
            'user_profile': user_profile,
            'is_profile_page': True,
            'is_google_account': is_google_account,
            'form_action': reverse('users:user_profile', args=(self.request.user,)),
            'search_form_action': reverse('training:search'),
            'additional_search_placeholder': 'na Home',
            'title': f'Perfil ({user})',
        })

    # get vai mostrar a foto de perfil do user e seus dados
    def get(self, *args, **kwargs):
        # 404 em tentativa de editar a url
        if self.kwargs.get('username') != self.request.user.username:  # type:ignore
            raise Http404()

        form = EditForm(instance=self.request.user)

        return self.render_form(form=form)

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
                # user não tem profile, contas que veem do google
                else:
                    UserProfile.objects.create(
                        user=self.request.user,
                        profile_picture=user_picture
                    )

            # salvando
            user.save()
            messages.success(
                self.request,
                'Dados Editados com Sucesso !'
            )
            return redirect(
                reverse('users:user_profile', args=(self.request.user,)),
            )

        return self.render_form(form=form)
