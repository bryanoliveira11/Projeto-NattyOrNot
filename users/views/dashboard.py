from os import environ
from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from training.models import Exercises
from utils.pagination import make_pagination

DASHBOARD_PER_PAGE = environ.get('DASHBOARD_PER_PAGE', 4)


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe base para o dashboard
class DashboardUserBase(ListView):
    template_name = 'users/pages/user_dashboard.html'
    model = Exercises
    context_object_name = 'user_exercises'
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        # filtrando exercícios que o usuário logado criou e não estão publicados
        queryset = queryset.filter(
            published_by=self.request.user,
        ).prefetch_related('categories')

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        # exercicios do contexto
        exercises = context.get('user_exercises')
        user = self.request.user

        # paginação
        page_obj, pagination_range = make_pagination(
            self.request, exercises, DASHBOARD_PER_PAGE
        )

        context.update({
            'exercises': page_obj,
            'pagination_range': pagination_range,
            'title': f'Dashboard',
            'page_tag': f'Meus Exercícios - Dashboard',
            'search_form_action': reverse('users:user_dashboard_search'),
            'is_dashboard_page': True,
            'placeholder': 'Pesquise por um Exercício ou Categoria',
            'additional_search_placeholder': 'no Dashboard',
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe para mostrar o dashboard do usuário com os exercícios criados
class DashboardUserClassView(DashboardUserBase):
    template_name = 'users/pages/user_dashboard.html'


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe para filtrar exercícios por categoria dentro da dashboard
class DashboardUserCategoryClassView(DashboardUserBase):
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            categories__id=self.kwargs.get('id'),
            published_by=self.request.user,
        )

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        user_exercises = context.get('user_exercises', '')
        user = self.request.user
        category_name = user_exercises[0].categories.filter(
            id=self.kwargs.get('id')
        ).first()

        context.update({
            'title': f'Dashboard - {category_name}',
            'page_tag': f'Meus Exercícios de {category_name} - Dashboard',
            'is_filtered': True,
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe para a barra de search do dashboard filtrar no dashboard em si, não na home.
class DashboardSearchClassView(DashboardUserBase):
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
                Q(published_by=self.request.user,
                  title__icontains=self.search_term) |
                Q(categories__name__icontains=self.search_term)
            )
        )

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        title = f'Dashboard - Pesquisa por "{self.search_term}"'

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
class DashboardIsPublishedFilterClassView(DashboardUserBase):
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        is_published = self.kwargs.get('is_published')

        queryset = queryset.filter(
            published_by=self.request.user, is_published=is_published
        )

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        is_published = self.kwargs.get('is_published')
        publish_translate = 'Públicados' if is_published == 'True' else 'Não Públicados'

        title = f'Meus Exercícios {publish_translate} - Dashboard'

        context.update({
            'title': title,
            'page_tag': title,
            'is_filtered': True,
        })

        return context
