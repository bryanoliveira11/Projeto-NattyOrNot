from os import environ
from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from training.models import Categories, Exercises
from utils.get_notifications import get_notifications
from utils.pagination import make_pagination

FAVORITES_PER_PAGE = environ.get('FAVORITES_PER_PAGE', 4)


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe base para a tela de favoritos
class FavoriteExercisesBaseClassView(ListView):
    template_name = 'users/pages/user_favorites.html'
    model = Exercises
    context_object_name = 'favorite_exercises'
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        # filtrando exercícios favoritados
        queryset = queryset.filter(
            favorited_by=self.request.user
        ).prefetch_related(
            'categories', 'favorited_by',
        ).select_related('published_by')

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        # exercicios do contexto
        exercises = context.get('favorite_exercises')
        categories = Categories.objects.all()
        results = len(exercises) if exercises else None
        title = 'Favoritos > Exercícios'

        # paginação
        page_obj, pagination_range = make_pagination(
            self.request, exercises, FAVORITES_PER_PAGE
        )

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'exercises': page_obj,
            'pagination_range': pagination_range,
            'categories': categories,
            'results_count': results,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': title,
            'page_tag': title,
            'search_form_action': reverse('users:user_dashboard_search'),
            'is_favorites_page': True,
            'placeholder': 'Pesquisar em Favoritos',
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe para filtrar exercícios por categoria nos favoritos
class FavoriteExercisesCategoriesFilter(FavoriteExercisesBaseClassView):
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            favorited_by=self.request.user,
            categories__id=self.kwargs.get('id'),
        )

        if not queryset:
            self.category = Categories.objects.filter(
                pk=self.kwargs.get('id')
            ).first()

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        favorite_exercises = context.get('favorite_exercises', '')

        try:
            category_name = favorite_exercises[0].categories.filter(
                id=self.kwargs.get('id')
            ).first()
        except IndexError:
            category_name = self.category.name if self.category else None

        if category_name is None:
            raise Http404()

        favorites = f'Favoritos > Exercícios > {category_name}'

        context.update({
            'title': favorites,
            'page_tag': favorites,
            'is_filtered': True,
        })

        return context
