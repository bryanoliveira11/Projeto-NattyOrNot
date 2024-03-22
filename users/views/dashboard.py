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

DASHBOARD_PER_PAGE = environ.get('DASHBOARD_PER_PAGE', 8)


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

        # filtrando exercícios que o usuário criou
        queryset = queryset.filter(
            published_by=self.request.user,
        ).prefetch_related('categories')

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        # exercicios do contexto
        exercises = context.get('user_exercises')
        categories = Categories.objects.all()
        results = len(exercises) if exercises else None

        # paginação
        page_obj, pagination_range = make_pagination(
            self.request, exercises, DASHBOARD_PER_PAGE
        )

        notifications, notifications_total = get_notifications(self.request)

        context.update({
            'exercises': page_obj,
            'pagination_range': pagination_range,
            'categories': categories,
            'results_count': results,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': 'Dashboard',
            'page_tag': 'Dashboard > Meus Exercícios',
            'search_form_action': reverse('users:user_dashboard_search'),
            'is_dashboard_page': True,
            'placeholder': 'Pesquisar no Dashboard',
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
            self.category = Categories.objects.filter(
                pk=self.kwargs.get('id')
            ).first()

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        user_exercises = context.get('user_exercises', '')

        try:
            category_name = user_exercises[0].categories.filter(
                id=self.kwargs.get('id')
            ).first()
        except IndexError:
            category_name = self.category.name if self.category else None

        if category_name is None:
            raise Http404()

        context.update({
            'title': f'Dashboard > Categoria > {category_name}',
            'page_tag': f'Dashboard > Meus Exercícios > {category_name}',
            'is_filtered': True,
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe para a barra de search do dashboard
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
                Q(title__icontains=self.search_term) |
                Q(categories__name__icontains=self.search_term)
            )
        ).distinct()

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        title = f'Dashboard > Busca > "{self.search_term}"'

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
class DashboardSharedStatusFilterClassView(DashboardUserBase):
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        shared_status = self.kwargs.get('shared_status')

        if shared_status not in ['MYSELF', 'FOLLOWERS', 'ALL']:
            raise Http404()

        queryset = queryset.filter(
            published_by=self.request.user, shared_status=shared_status
        )

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        shared_status = self.kwargs.get('shared_status')

        shared_translate = {
            'MYSELF': 'Apenas Você',
            'FOLLOWERS': 'Meus Seguidores',
            'ALL': 'Todos',
        }

        title = f'Dashboard > Visibilidade > {
            shared_translate.get(shared_status)
        }'

        context.update({
            'title': title,
            'page_tag': title,
            'is_filtered': True,
        })

        return context
