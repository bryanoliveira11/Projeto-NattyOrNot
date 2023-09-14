from typing import Any

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from training.models import Exercises


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


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe para mostrar o dashboard do usuário com os exercícios criados
class DashboardUserClassView(DashboardUserBase):
    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        # pegando exercícios que vieram da query no contexto
        user_exercises = context.get('user_exercises')
        user = self.request.user

        # passando o resultado da queryset para a key exercises usada no template html
        context.update({
            'exercises': user_exercises,
            'title': f'Dashboard de {user}',
            'page_tag': f'Meus Exercícios - Dashboard ({user})',
            'is_dashboard_page': True,
        })

        return context


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
            'exercises': user_exercises,
            'title': f'Dashboard de {user}',
            'page_tag': f'Meus Exercícios de {category_name} - Dashboard ({user})',
            'is_dashboard_page': True,
        })

        return context
