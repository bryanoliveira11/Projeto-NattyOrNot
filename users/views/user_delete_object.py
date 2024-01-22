from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView

from training.models import Exercises
from users.models import UserWorkouts
from utils.get_notifications import get_notifications


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserObjectExerciseDeleteClassView(DetailView):
    model = Exercises
    template_name = 'users/partials/delete_page.html'
    context_object_name = 'user_exercise'
    pk_url_kwarg = 'id'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            published_by=self.request.user, is_published=False
        )
        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        exercise = context.get('user_exercise')
        title = f'Deletar Exercício - {exercise}'

        if exercise:
            form_action = reverse(
                'users:user_exercise_delete_confirm', args=(exercise.pk,)
            )
        else:
            raise Http404()

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'exercise': exercise,
            'form_action': form_action,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': title,
            'search_form_action': reverse('users:user_dashboard_search'),
            'is_exercise': True,
            'placeholder': 'Pesquise por um Exercício ou Categoria',
            'additional_search_placeholder': 'no Dashboard',
            'type_of_object': 'Exercício',
            'has_cover': True,
        })
        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserObjectWorkoutDeleteClassView(DetailView):
    model = UserWorkouts
    template_name = 'users/partials/delete_page.html'
    context_object_name = 'user_workout'
    pk_url_kwarg = 'id'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user_id=self.request.user)

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        workout = context.get('user_workout')
        title = f'Deletar Treino - {workout.title}' if workout else workout

        if workout:
            form_action = reverse(
                'users:user_workout_delete_confirm', args=(workout.pk,)
            )
        else:
            raise Http404()

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'exercise': workout,
            'workout': workout,
            'notifications': notifications,
            'notification_total': notifications_total,
            'form_action': form_action,
            'title': title,
            'search_form_action': reverse('users:user_workouts_search'),
            'placeholder': 'Pesquise por um Treino',
            'is_workout_page': True,
            'type_of_object': 'Treino',
            'has_cover': True,
        })
        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class DeleteObjectClassViewBase(View):
    def get_exercise(self, id=None):
        exercise = None

        if id is not None:
            exercise = Exercises.objects.filter(
                published_by=self.request.user,
                pk=id,
                is_published=False,
            ).first()

            if not exercise:
                raise Http404()

        return exercise

    def delete_object(self, type: str, msg_obj: str):
        obj = None

        if type == 'exercise':
            obj = self.get_exercise(self.request.POST.get('id'))

        if type == 'workout':
            obj = UserWorkouts.objects.filter(
                pk=self.request.POST.get('id')).first()

        if obj:
            messages.success(
                self.request,
                f'{msg_obj} Deletado com Sucesso.'
            )
            obj.delete()


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class DeleteExerciseClassView(DeleteObjectClassViewBase):
    def get(self, *args, **kwargs):
        return redirect(reverse('users:user_dashboard'))

    def post(self, *args, **kwargs):
        self.delete_object(type='exercise', msg_obj='Exercício')
        return redirect(reverse('users:user_dashboard'))


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class DeleteWorkoutClassView(DeleteObjectClassViewBase):
    def get(self, *args, **kwargs):
        return redirect('users:user_workouts')

    def post(self, *args, **kwargs):
        self.delete_object(type='workout', msg_obj='Treino')
        return redirect(reverse('users:user_workouts'))
