from os import environ
from typing import Any

from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from users.forms import ChangePasswordForm, CreateWorkoutForm, EditForm
from users.models import UserProfile, UserWorkouts
from utils.pagination import make_pagination

User = get_user_model()
WORKOUT_PER_PAGE = environ.get('WORKOUT_PER_PAGE', 10)


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

    def validate_url_user(self, username):
        # 404 em tentativa de editar a url
        if username != self.request.user.username:  # type:ignore
            raise Http404()

    def get_profile_form_action(self):
        return reverse('users:user_profile', args=(self.request.user,))

    def get_password_change_form_action(self):
        return reverse('users:user_profile_change_password', args=(self.request.user,))

    def render_form(self, form, form_action, profile_page=False, password_page=False):
        user = self.request.user
        user_profile = self.get_user_profile(user.pk)
        is_google_account = self.is_google_account_user()

        return render(self.request, 'users/pages/user_profile.html', context={
            'user': user,
            'form': form,
            'user_profile': user_profile,
            'is_google_account': is_google_account,
            'is_profile_page': profile_page,
            'is_change_password_page': password_page,
            'form_action': form_action,
            'search_form_action': reverse('training:search'),
            'additional_search_placeholder': 'na Home',
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


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutsPageClassView(ListView):
    template_name = 'users/pages/user_workout.html'
    model = UserWorkouts
    context_object_name = 'user_workout'
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            user=self.request.user
        ).select_related('user')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        workouts = context.get('user_workout')
        titles = f'Meus Treinos ({self.request.user})'

        # paginação
        page_obj, pagination_range = make_pagination(
            self.request, workouts, WORKOUT_PER_PAGE
        )

        context.update({
            'workouts': page_obj,
            'exercises': page_obj,  # for paginations to work
            'pagination_range': pagination_range,
            'search_form_action': reverse('training:search'),
            'additional_search_placeholder': 'na Home',
            'is_workout_page': True,
            'page_tag': titles,
            'title': titles,
        })

        return context


class UserWorkoutBaseClass(View):
    def get_workout(self, id=None):
        workout = None

        # verificando se há um id na url, se tiver, significa que é uma edição
        if id is not None:
            # validando se foi publicado pelo usuário logado
            workout = UserWorkouts.objects.filter(
                user=self.request.user,
                pk=id,
            ).first()

            # lançando erro 404 caso não tenha nenhum resultado para o id
            if not workout:
                raise Http404()

            # variáveis para controlar título e mensagens ao usuário
            self.title = f'Editar Treino - {workout.title}'
            self.is_workout_edit = True
        else:
            self.title = 'Criar Treino'
            self.is_workout_edit = False

        return workout

    def render_workout(self, form):  # renderizando página do form
        return render(self.request, 'users/pages/create_workout.html', context={
            'form': form,
            'search_form_action': reverse('users:user_dashboard_search'),
            'title': self.title,
            'captcha_public_key': environ.get('RECAPTCHA_PUBLIC_KEY', ''),
            'captcha_private_key': environ.get('RECAPTCHA_PRIVATE_KEY', ''),
            'is_workout_form': True,
            'is_workout_edit': self.is_workout_edit,
        })


class UserWorkoutClassView(UserWorkoutBaseClass):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = None

    def get(self, request, id=None):
        workout = self.get_workout(id)
        form = CreateWorkoutForm(instance=workout)
        return self.render_workout(form=form)

    def post(self, request, id=None):
        workout = self.get_workout(id)

        form = CreateWorkoutForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=workout
        )

        if form.is_valid():
            workout = form.save(commit=False)
            # garantindo o usuário que registrou
            workout.user = request.user
            workout.exercises_total = len(
                form.cleaned_data.get('exercises').all()
            )
            # salvando no banco
            workout.save()
            # garantindo o preenchimento dos exercícios pós save
            workout.exercises.set(form.cleaned_data.get('exercises').all())

            if self.is_workout_edit:
                messages.success(request, 'Treino Editado com Sucesso !')
            else:
                messages.success(request, 'Treino Criado com Sucesso !')

            return redirect(reverse('users:user_workout_edit', args=(workout.pk,)))

        return self.render_workout(form=form)
