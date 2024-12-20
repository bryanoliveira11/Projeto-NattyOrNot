import json

from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from training.models import Exercises
from users.forms import ChangePasswordForm, EditForm, UserHealthForm
from users.models import (UserFollows, UserHealth, UserHealthChartData,
                          UserProfile)
from utils.get_notifications import get_notifications
from utils.get_profile_picture import get_profile_picture
from utils.imc_classify import imc_classify
from utils.pagination import make_pagination
from utils.user_utils import get_user_follow_stats

User = get_user_model()


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserProfileBaseClassView(View):
    def get_user_profile_by_id(self, user_id: int) -> UserProfile | None:
        return UserProfile.objects.filter(user__id=user_id).first()

    def get_user_profile_by_name(self, username: str) -> UserProfile | None:
        return UserProfile.objects.filter(user__username=username).first()

    def get_user_instance(self, username: str):
        return User.objects.filter(username=username).first()

    def is_google_account_user(self) -> bool:
        google_account = EmailAddress.objects.filter(
            user_id=self.request.user.pk
        ).first()

        if google_account is not None:
            return True
        return False

    # lançar um alerta na tela de perfil se o email do usuário estiver vázio
    # isso ocorre se a conta for do google e o email já estiver em uso
    def check_email(self) -> None:
        user_db = User.objects.filter(pk=self.request.user.pk).first()

        if user_db:
            if not user_db.email:  # type:ignore
                messages.warning(
                    self.request,
                    'Seu E-mail não está Preenchido. '
                    'Por Favor, Revise seus Dados !'
                )

    def validate_url_user(self, username: str):
        # 404 em tentativa de editar a url
        if username != self.request.user.get_username():
            raise Http404()

    def get_profile_form_action(self) -> str:
        return reverse('users:user_profile_data', args=(self.request.user,))

    def get_password_change_form_action(self) -> str:
        return reverse(
            'users:user_profile_change_password', args=(self.request.user,)
        )

    def get_user_exercises(self, user):
        exercises = Exercises.objects.filter(
            published_by=user,
        ).exclude(shared_status='MYSELF').select_related(
            'published_by'
        ).prefetch_related('categories', 'favorited_by').order_by('-pk')

        return exercises

    def render_form(
        self, form, form_action='', profile_page=False, password_page=False
    ) -> HttpResponse:
        user = self.request.user
        user_profile = self.get_user_profile_by_id(user.pk)  # type:ignore
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
            'title': f'Meus Dados - {user}',
        })


# classe para o perfil publico
class UserShowProfileClassView(View):
    def get(self, *args, **kwargs):
        user_instance = User.objects.filter(
            username=self.kwargs.get('username')
        ).first()

        user_profile = UserProfile.objects.filter(
            user=user_instance,
        ).select_related('user').first()

        if user_profile is None or not user_instance:
            raise Http404()

        notifications, notifications_total = get_notifications(self.request)

        already_follows = False

        if self.request.user.is_authenticated:
            if self.kwargs.get('username') != self.request.user.username:
                already_follows = UserFollows.objects.filter(
                    follower=self.request.user, following=user_instance
                ).exists()

        exercises = Exercises.objects.filter(
            published_by=user_instance,
        ).prefetch_related(
            'published_by', 'categories'
        ).order_by('-pk').exclude(
            shared_status='MYSELF',
        )

        if not already_follows:
            exercises = exercises.exclude(
                shared_status__in=['MYSELF', 'FOLLOWERS']
            )

        page_obj, pagination_range = make_pagination(
            self.request, exercises, 12
        )

        follower_count, following_count = get_user_follow_stats(
            user_instance.pk
        )  # type: ignore

        user_health = UserHealth.objects.filter(
            user=user_instance,
        ).first()

        return render(
            self.request, 'users/pages/user_show_profile.html', context={
                'user_profile': user_profile,
                'user': user_instance,
                'user_health': user_health,
                'exercises': page_obj,
                'pagination_range': pagination_range,
                'notifications': notifications,
                'notification_total': notifications_total,
                'title': f'Perfil - {user_profile}',
                'already_follows': already_follows,
                'follower_count': follower_count,
                'following_count': following_count,
            }
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserProfileDataClassView(UserProfileBaseClassView):
    # get vai mostrar a foto de perfil do user e seus dados
    def get(self, *args, **kwargs):
        self.validate_url_user(self.kwargs.get('username'))
        user_profile = self.get_user_profile_by_name(
            self.kwargs.get('username')
        )
        form = EditForm(user_profile=user_profile, instance=self.request.user)
        return self.render_form(
            form=form,
            profile_page=True,
            form_action=self.get_profile_form_action()
        )

    # post permitirá que o user edite os dados existentes da conta
    def post(self, *args, **kwargs):
        self.validate_url_user(self.kwargs.get('username'))

        form = EditForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.request.user
        )

        if form.is_valid():
            user = form.save(commit=False)
            user_picture = form.cleaned_data.get('profile_picture')
            user_profile = self.get_user_profile_by_id(
                self.request.user.pk  # type:ignore
            )

            # user já tem profile
            if user_profile:
                if user_picture:
                    # alterando foto caso haja dados no form
                    user_profile.profile_picture = user_picture
                user_profile.save()
                get_profile_picture(self.request, self.request.user)

            # salvando
            user.save()
            messages.success(
                self.request,
                'Dados Editados com Sucesso !'
            )
            return redirect(
                reverse('users:user_profile_data', args=(self.request.user,)),
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
class UserProfileChangePassword(UserProfileBaseClassView):
    def get(self, *args, **kwargs):
        self.validate_url_user(self.kwargs.get('username'))
        form = ChangePasswordForm(instance=self.request.user)
        return self.render_form(
            form=form,
            password_page=True,
            form_action=self.get_password_change_form_action()
        )

    def post(self, *args, **kwargs):
        self.validate_url_user(self.kwargs.get('username'))

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
class UserProfileHealthClassView(UserProfileBaseClassView):
    def get_health_data_chart(self):
        user_chart_data = UserHealthChartData.objects.filter(
            user=self.request.user
        ).all()

        if not user_chart_data:
            return

        weight_list = []
        date_list = []

        for data in user_chart_data:
            date = data.created_at.date()
            formated_date = date.strftime('%d/%m/%Y')
            weight_list.append(float(data.weight))
            date_list.append(formated_date)

        return {
            'weights': weight_list[::-1],
            'dates': date_list[::-1],
        }

    def render_health_form(self, form, user_health):
        title = f'Health - {self.request.user.get_username()}'
        notifications, notifications_total = get_notifications(self.request)
        imc_category, imc_css_class = imc_classify(
            user_health.imc
        ) if user_health.imc else (None, None)
        user_chart_data = self.get_health_data_chart()
        user_chart_data = json.dumps(
            user_chart_data, indent=1, ensure_ascii=False
        )
        chart_exists = True

        if user_chart_data == 'null':
            chart_exists = False

        return render(
            self.request,
            'users/pages/user_profile_health.html', context={
                'form': form,
                'user_health': user_health,
                'imc_category': imc_category,
                'imc_css_class': imc_css_class,
                'user_chart_data': user_chart_data,
                'chart_exists': chart_exists,
                'notifications': notifications,
                'notification_total': notifications_total,
                'title': title,
                'page_tag': title,
                'is_health_page': True
            })

    def get_health_user(self, username: str) -> UserHealth | None:
        return UserHealth.objects.filter(
            user__username=username
        ).select_related('user').first()

    def create_health_user(self):
        user = self.get_user_instance(self.kwargs.get('username'))
        user_health = self.get_health_user(
            user.get_username()
        ) if user else user

        if not (user_health):
            user_health = UserHealth.objects.create(user=user)

        return user_health

    def get(self, *args, **kwargs):
        self.validate_url_user(self.kwargs.get('username'))
        user_health = self.create_health_user()
        form = UserHealthForm(
            instance=user_health
        )

        return self.render_health_form(
            form=form,
            user_health=user_health
        )

    def post(self, *args, **kwargs):
        self.validate_url_user(self.kwargs.get('username'))
        user_health = self.get_health_user(self.kwargs.get('username'))

        form = UserHealthForm(
            data=self.request.POST or None,
            instance=user_health
        )

        if form.is_valid():
            user_health = form.save(commit=False)
            height = form.cleaned_data.get('height')
            weight = form.cleaned_data.get('weight')

            if height and weight:
                height = int(height)
                weight = float(weight)
                user_health.imc = round(
                    float(weight / (height / 100) ** 2), 2
                )
                user_health.protein_intake = float(weight * 0.8)
                user_health.water_intake = float(weight * 35)

            user_health.is_valid_data = True
            user_health.save()

            # criando dados para o chart.js
            UserHealthChartData.objects.create(
                user=user_health.user,
                weight=weight,
            )

            messages.success(
                self.request,
                'Dados Editados com Sucesso !'
            )
            return redirect(
                reverse(
                    'users:user_profile_health', args=(self.request.user,)
                ),
            )

        return self.render_health_form(
            form=form,
            user_health=user_health
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserProfileHealthDeleteLastData(View):
    def get(self, *args, **kwargs):
        return redirect(
            reverse(
                'users:user_profile_health', args=(self.request.user,)
            ),
        )

    def post(self, *args, **kwargs):
        last_chart_data = UserHealthChartData.objects.filter(
            user=self.request.user,
        ).first()

        if last_chart_data:
            last_chart_data.delete()
            messages.success(
                self.request, 'Último Registro de Peso Deletado com Sucesso.'
            )

        return redirect(
            reverse(
                'users:user_profile_health', args=(self.request.user,)
            ),
        )
