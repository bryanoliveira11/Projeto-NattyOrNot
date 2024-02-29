from os import environ
from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView

from users.forms import CreateWorkoutForm
from users.models import UserWorkouts
from utils.get_notifications import get_notifications
from utils.pagination import make_pagination

WORKOUT_PER_PAGE = environ.get('WORKOUT_PER_PAGE', 5)


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
        titles = f'Meus Treinos'

        # paginação
        page_obj, pagination_range = make_pagination(
            self.request, workouts, WORKOUT_PER_PAGE
        )

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'workouts': page_obj,
            'exercises': page_obj,  # for paginations to work
            'notifications': notifications,
            'notification_total': notifications_total,
            'pagination_range': pagination_range,
            'search_form_action': reverse('users:user_workouts_search'),
            'placeholder': 'Pesquise por um Treino',
            'is_workout_page': True,
            'page_tag': titles,
            'title': titles,
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutsPageDetailClassView(DetailView):
    template_name = 'users/pages/user_workout_detail.html'
    model = UserWorkouts
    context_object_name = 'workout_detail'
    pk_url_kwarg = 'id'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user).select_related('user').prefetch_related(
            'exercises', 'exercises__categories', 'exercises__published_by'
        )
        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        workout = context.get('workout_detail')
        title = workout.title if workout else workout
        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'workout': workout,
            'notifications': notifications,
            'notification_total': notifications_total,
            'search_form_action': reverse('training:search'),
            'title': f'{title}',
            'page_tag': f'{title}',
            'search_form_action': reverse('users:user_workouts_search'),
            'placeholder': 'Pesquise por um Treino',
            'is_detail_page': True,
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutsPageSearchClassView(UserWorkoutsPageClassView):
    def __init__(self, *args, **kwargs):
        self.search_term = ''
        return super().__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)
        self.search_term = self.request.GET.get('q', '').strip()

        if not self.search_term:
            raise Http404()

        queryset = queryset.filter(
            Q
            (
                Q(title__icontains=self.search_term) |
                Q(exercises_total__icontains=self.search_term)
            )
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        title = f'Meus Treinos - Pesquisa por "{self.search_term}"'

        context.update({
            'title': title,
            'page_tag': title,
            'additional_url_query': f'&q={self.search_term}',
            'is_filtered': True,
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutBaseClass(View):
    def get_workout(self, id=None):
        workout = None

        # verificando se há um id na url, se tiver, significa que é uma edição
        if id is not None:
            # validando se foi publicado pelo usuário logado
            workout = UserWorkouts.objects.filter(
                user=self.request.user,
                pk=id,
            ).select_related('user').first()

            # lançando erro 404 caso não tenha nenhum resultado para o id
            if not workout:
                raise Http404()

            # variáveis para controlar título e mensagens ao usuário
            self.title = f'Editar Treino - {workout.title}'
            self.is_workout_edit = True
        else:
            self.title = 'Novo Treino'
            self.is_workout_edit = False

        return workout

    def get_referer_url(self):
        http_referer = self.request.META.get('HTTP_REFERER')
        create_url = reverse('users:user_workout_create')

        if http_referer is None or self.request.path in http_referer or create_url in http_referer:
            print('cheguei no if')
            url_to_redirect = reverse(
                'users:user_workouts'
            )
        else:
            url_to_redirect = http_referer

        return url_to_redirect

    def render_workout(self, form):  # renderizando página do form
        notifications, notifications_total = get_notifications(self.request)

        url_to_redirect = self.get_referer_url()

        return render(self.request, 'users/pages/create_workout.html', context={
            'form': form,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': self.title,
            'captcha_public_key': environ.get('RECAPTCHA_PUBLIC_KEY', ''),
            'captcha_private_key': environ.get('RECAPTCHA_PRIVATE_KEY', ''),
            'is_workout_form': True,
            'is_workout_edit': self.is_workout_edit,
            'url_to_redirect': url_to_redirect,
            'search_form_action': reverse('users:user_workouts_search'),
            'placeholder': 'Pesquise por um Treino',
        })


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
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
            # garantindo o preenchimento do usuário
            workout.user = request.user
            # pegando a quantidade de exercícios escolhidos no form
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


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutShareClassView(View):
    def get_workout(self):
        workout = UserWorkouts.objects.filter(
            pk=self.kwargs.get('id'),
            user_id=self.request.user
        ).select_related('user').first()

        if not workout:
            raise Http404()

        return workout

    def get(self, *args, **kwargs):
        workout = self.get_workout()

        # garantindo que o treino não está compartilhado
        if workout.is_shared:
            messages.error(
                self.request,
                'Este Treino já Está Compartilhado.'
            )
            return redirect(reverse('users:user_workouts'))

        title = workout.title if workout else workout

        notifications, notifications_total = get_notifications(self.request)

        return render(self.request, 'users/partials/share_page.html', {
            'exercise': workout,
            'workout': workout,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': f'Compartilhar Treino - {title}',
            'search_form_action': reverse('users:user_workouts_search'),
            'placeholder': 'Pesquise por um Treino',
            'is_workout_page': True,
        })

    def post(self, *args, **kwargs):
        workout = self.get_workout()

        if workout:
            # garantindo que o usuário é o mesmo
            if workout.user != self.request.user:
                messages.error(
                    self.request,
                    'Um Erro Ocorreu ao Compartilhar o Treino. Tente Novamente.'
                )
                return redirect(reverse('users:user_workouts'))

            # compartilhando treino
            workout.is_shared = True
            workout.save()
            messages.success(
                self.request,
                'Treino Compartilhado com Sucesso.'
            )

        return redirect(reverse('users:user_workouts'))


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutUnshareClassView(UserWorkoutShareClassView):
    def get(self, *args, **kwargs):
        workout = self.get_workout()

        # garantindo que o treino está compartilhado
        if not workout.is_shared:
            messages.error(
                self.request,
                'Este Treino Não Está Compartilhado.'
            )
            return redirect(reverse('users:user_workouts'))

        title = workout.title if workout else workout

        notifications, notifications_total = get_notifications(self.request)

        return render(self.request, 'users/partials/share_page.html', {
            'exercise': workout,
            'workout': workout,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': f'Remover Compartilhamento do Treino - {title}',
            'search_form_action': reverse('users:user_workouts_search'),
            'placeholder': 'Pesquise por um Treino',
            'is_workout_page': True,
        })

    def post(self, *args, **kwargs):
        workout = self.get_workout()

        if workout:
            # garantindo que o usuário é o mesmo
            if workout.user != self.request.user:
                messages.error(
                    self.request,
                    'Um Erro Ocorreu. Tente Novamente.'
                )
                return redirect(reverse('users:user_workouts'))

            # compartilhando treino
            workout.is_shared = False
            workout.save()
            messages.success(
                self.request,
                'Compartilhamento Removido com Sucesso.'
            )

        return redirect(reverse('users:user_workouts'))


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutsIsSharedFilterClassView(UserWorkoutsPageClassView):
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        is_shared = self.kwargs.get('is_shared')

        if is_shared not in ['True', 'False']:
            raise Http404()

        queryset = queryset.filter(
            user=self.request.user,
            is_shared=is_shared
        ).select_related('user')

        if not queryset:
            messages.error(self.request, 'Nenhum Treino Encontrado.')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        is_shared = self.kwargs.get('is_shared')
        publish_translate = 'Publicados' if is_shared == 'True' else 'Não Publicados'

        title = f'Filtrando por Treinos {publish_translate}'

        context.update({
            'title': title,
            'page_tag': title,
            'is_filtered': True,
        })

        return context
