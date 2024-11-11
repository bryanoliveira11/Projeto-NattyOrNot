from typing import Any, Dict

from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

from training.contexts.training_base_contexts import get_home_page_base_context
from users.models import UserProfile, UserWorkouts
from utils.pagination import make_pagination


class GlobalWorkoutsClassView(ListView):
    template_name = 'users/pages/global_workouts.html'
    context_object_name = 'global_workouts'
    ordering = ['-id']
    model = UserWorkouts

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            shared_status='ALL',
        ).select_related('user').prefetch_related('exercises')

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        workouts: list[QuerySet] = context.get('global_workouts') or []

        results = len(workouts) if workouts else None
        title = 'Treinos Publicados'

        page_obj, pagination_range = make_pagination(
            self.request, workouts, 10
        )

        user_list = [
            workout.user for workout in  # type:ignore
            workouts if workout.user  # type:ignore
        ]

        user_profiles = UserProfile.objects.filter(
            user__in=user_list
        ).select_related('user')

        users_data = {
            profile.user: f'media/{profile.profile_picture}'
            for profile in user_profiles
        }

        context.update({
            'workouts': page_obj,
            'page_obj': page_obj,
            'users_data': users_data,
            'results_count': results,
            'pagination_range': pagination_range,
            'title': title,
            'page_tag': title,
            'is_workout_page': True,
        })

        return context
