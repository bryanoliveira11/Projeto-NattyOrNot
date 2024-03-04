from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
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
class UserExerciseDeleteClassView(DetailView):
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

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'exercise': exercise,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': title,
            'is_exercise': True,
            'type_of_object': 'Exercício',
            'has_cover': True,
        })
        return context

    def post(self, *args, **kwargs):
        # pegando o exercicio do banco
        exercise_to_delete = Exercises.objects.filter(
            pk=self.kwargs.get('id'),
            published_by=self.request.user,
            is_published=False,
        ).first()

        # não encontrou no banco
        if not exercise_to_delete:
            messages.error(
                self.request,
                'Um Erro Ocorreu ao Deletar o Exercício.'
            )
            return redirect(reverse('users:user_dashboard'))

        # deletando exercício
        exercise_to_delete.delete()
        messages.success(
            self.request,
            'Exercício Deletado com Sucesso.'
        )

        return redirect(reverse('users:user_dashboard'))


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutDeleteClassView(DetailView):
    model = UserWorkouts
    template_name = 'users/partials/delete_page.html'
    context_object_name = 'user_workout'
    pk_url_kwarg = 'id'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            user_id=self.request.user
        ).select_related('user')

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        workout = context.get('user_workout')
        title = f'Deletar Treino - {workout.title}' if workout else workout

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'exercise': workout,
            'workout': workout,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': title,
            'is_workout_page': True,
            'type_of_object': 'Treino',
            'has_cover': True,
        })
        return context

    def post(self, *args, **kwargs):
        # pegando o treino do banco
        workout_to_delete = UserWorkouts.objects.filter(
            pk=self.kwargs.get('id'),
            user=self.request.user,
        ).first()

        if not workout_to_delete:
            messages.error(
                self.request,
                'Um Erro Ocorreu ao Deletar o Treino.'
            )
            return redirect(reverse('users:user_workouts'))

        # deletando treino
        workout_to_delete.delete()
        messages.success(
            self.request,
            'Treino Deletado com Sucesso.'
        )

        return redirect(reverse('users:user_workouts'))
