from os import environ
from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
            'title': f'Dashboard de {user}',
            'page_tag': f'Meus Exercícios - Dashboard ({user})',
            'search_form_action': reverse('users:user_dashboard_search'),
            'is_dashboard_page': True,
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
            'title': f'Dashboard de {user} - {category_name}',
            'page_tag': f'Meus Exercícios de {category_name} - Dashboard ({user})',
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
            published_by=self.request.user, title__icontains=self.search_term
        )

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        title = f'Dashboard ({self.request.user}) - Pesquisa por "{self.search_term}"'

        context.update({
            'title': title,
            'page_tag': title,
        })

        return context


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

        if is_published == 'False':
            publish_translate = 'Não Públicados'
        else:
            publish_translate = 'Públicados'

        title = f'Meus Exercícios {publish_translate} - Dashboard ({self.request.user})'

        context.update({
            'title': title,
            'page_tag': title,
        })

        return context
