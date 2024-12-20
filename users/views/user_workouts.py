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
        titles = 'Meus Treinos'

        results = len(workouts) if workouts else None

        # paginação
        page_obj, pagination_range = make_pagination(
            self.request, workouts, WORKOUT_PER_PAGE
        )

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'workouts': page_obj,
            'exercises': page_obj,  # for paginations to work
            'results_count': results,
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
        queryset = queryset.select_related('user').prefetch_related(
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
            'title': f'{title}',
            'page_tag': f'{title}',
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

        title = f'Meus Treinos - Busca por "{self.search_term}"'

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
            self.title = f'Editar Treino > {workout.title}'
            self.is_workout_edit = True
        else:
            self.title = 'Novo Treino'
            self.is_workout_edit = False

        return workout

    def get_referer_url(self):
        referer = self.request.META.get('HTTP_REFERER')
        workout = reverse('users:user_workout_create')
        req_path = self.request.path

        if referer is None or req_path in referer or workout in referer:
            url_to_redirect = reverse(
                'users:user_workouts'
            )
        else:
            url_to_redirect = referer

        return url_to_redirect

    def render_workout(self, form):  # renderizando página do form
        notifications, notifications_total = get_notifications(self.request)

        url_to_redirect = self.get_referer_url()

        return render(
            self.request, 'users/pages/create_workout.html',
            context={
                'form': form,
                'notifications': notifications,
                'notification_total': notifications_total,
                'title': self.title,
                'captcha_public_key': environ.get(
                    'RECAPTCHA_PUBLIC_KEY', ''
                ),
                'captcha_private_key': environ.get(
                    'RECAPTCHA_PRIVATE_KEY', ''
                ),
                'is_workout_form': True,
                'is_workout_edit': self.is_workout_edit,
                'url_to_redirect': url_to_redirect,
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
        exercises_initial = workout.exercises.all() if workout else None
        form = CreateWorkoutForm(
            instance=workout, initial={'exercises': exercises_initial}
        )
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
            exercises = form.cleaned_data.get('exercises')

            if not exercises:
                return

            workout.exercises_total = len(
                exercises.all()
            )
            # salvando no banco
            workout.save()
            # garantindo o preenchimento dos exercícios pós save
            workout.exercises.set(exercises.all())

            if self.is_workout_edit:
                messages.success(request, 'Treino Editado com Sucesso !')
            else:
                messages.success(request, 'Treino Criado com Sucesso !')

            return redirect(
                reverse('users:user_workout_edit', args=(workout.pk,))
            )

        return self.render_workout(form=form)


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutsIsSharedFilterClassView(UserWorkoutsPageClassView):
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        shared_status = self.kwargs.get('shared_status')

        if shared_status not in ['MYSELF', 'ALL']:
            raise Http404()

        queryset = queryset.filter(
            user=self.request.user,
            shared_status=shared_status
        ).select_related('user')

        if not queryset:
            messages.error(self.request, 'Nenhum Treino Encontrado.')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        shared_status = self.kwargs.get('shared_status')
        translated = 'Compartilhados' if shared_status == 'ALL' \
            else 'Não Compartilhados'

        title = f'Treinos - {translated}'

        context.update({
            'title': title,
            'page_tag': title,
            'is_filtered': True,
        })

        return context
