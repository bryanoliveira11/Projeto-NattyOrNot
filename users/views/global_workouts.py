from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View

from users.models import UserProfile, UserWorkouts
from utils.get_notifications import get_notifications
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

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'workouts': page_obj,
            'exercises': page_obj,
            'users_data': users_data,
            'results_count': results,
            'pagination_range': pagination_range,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': title,
            'page_tag': title,
            'is_workout_page': True,
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserWorkoutsFavoritesClassView(ListView):
    template_name = 'users/pages/user_workouts_favorites.html'
    model = UserWorkouts
    context_object_name = 'user_workout_favorites'
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            favorited_by=self.request.user
        ).select_related('user')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        workouts = context.get('user_workout_favorites')
        titles = 'Treinos Favoritos'

        results = len(workouts) if workouts else None

        # paginação
        page_obj, pagination_range = make_pagination(
            self.request, workouts, 12
        )

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'workouts': page_obj,
            'exercises': page_obj,
            'results_count': results,
            'notifications': notifications,
            'notification_total': notifications_total,
            'pagination_range': pagination_range,
            'search_form_action': reverse('users:user_workouts_search'),
            'placeholder': 'Pesquise por um Treino',
            'is_workout_favorites_page': True,
            'page_tag': titles,
            'title': titles,
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class FavoriteWorkoutClassView(View):
    def get(self, *args, **kwargs):
        workout_id = self.kwargs.get('id', '')
        workout = UserWorkouts.objects.filter(pk=workout_id).first()
        user = self.request.user
        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('training:home')
        )
        favorites_url = reverse('users:user_workouts_favorites')
        msg_url = f'''<a class="favorites-url" href="{favorites_url}"
              title="Ver Favoritos"> Ver Favoritos
              <i class="fa-solid fa-star" style="font-size:1.8rem;"></i>
              </a>'''

        if not workout:
            return redirect(http_referer)

        if user in workout.favorited_by.all():
            workout.favorited_by.remove(user)
            workout.save()
            messages.success(
                self.request,
                f'''Treino desfavoritado. {msg_url}'''
            )
            return redirect(http_referer)

        workout.favorited_by.add(user)
        workout.save()

        messages.success(
            self.request,
            f'''Treino favoritado com sucesso! {msg_url}'''
        )

        return redirect(http_referer)
