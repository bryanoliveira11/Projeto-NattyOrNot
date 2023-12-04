from typing import Any

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
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
