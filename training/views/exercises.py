from os import environ
from typing import Any, Dict

from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView

from training.models import Exercises
from utils.pagination import make_pagination

PER_PAGE = environ.get('HOME_PER_PAGE', 8)

# classe base para a home


class ExerciseBaseClassView(ListView):
    template_name = 'training/pages/home.html'
    context_object_name = 'training'
    ordering = ['-id']
    model = Exercises

    # filtrando exercícios que estejam publicados e otimizando a consulta sql
    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(is_published=True).select_related(
            'published_by').prefetch_related('categories')

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        exercises = context.get('training')

        # paginação
        page_obj, pagination_range = make_pagination(
            self.request, exercises, PER_PAGE
        )

        context.update({
            'exercises': page_obj,
            'pagination_range': pagination_range,
            'search_form_action': reverse('training:search'),
            'title': 'Home',
            'page_tag': 'Exercícios'
        })

        return context


# classe para a homepage
class HomeClassView(ExerciseBaseClassView):
    template_name = 'training/pages/home.html'


# classe para a barra de pesquisa
class SearchClassView(ExerciseBaseClassView):
    template_name = 'training/pages/home.html'

    def __init__(self, *args, **kwargs) -> None:
        self.search_term = None
        super().__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        queryset = super().get_queryset(*args, **kwargs)
        self.search_term = self.request.GET.get('q', '').strip()

        # lançando um 404 not found caso não haja nada na pesquisa
        if not self.search_term:
            raise Http404()

        # filtrando no banco de dados
        queryset = queryset.filter(
            Q(
                Q(title__icontains=self.search_term)
            ),
            is_published=True
        )
        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'title': f'Busca por "{self.search_term}"',
            'page_tag': f'Resultados da Busca por "{self.search_term}"',
            'additional_url_query': f'&q={self.search_term}',
            'is_home_page': True,
            'is_filtered': True,
        })
        return context


# classe para filtrar por categoria
class CategoriesFilterClassView(ExerciseBaseClassView):
    template_name = 'training/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        # consulta no banco de dados
        queryset = queryset.filter(
            categories__id=self.kwargs.get('id'),
            is_published=True)

        # 404 se não existir o id da categoria no banco
        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        # filtrando no banco para obter no nome da categoria com base no id
        category_name = context.get('training', '')[0].categories.filter(
            id=self.kwargs.get('id')
        ).first()

        context.update({
            'title': f'Categoria - {category_name}',
            'page_tag': f'Filtrando por Exercícios de {category_name}',
            'is_filtered': True,
        })

        return context
