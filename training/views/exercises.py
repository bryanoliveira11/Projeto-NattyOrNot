import json
from os import environ
from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View

from training.contexts.training_base_contexts import get_home_page_base_context
from training.models import ApiMediaImages, Categories, Exercises
from utils.api_exercises_json import exercises_json
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

        queryset = queryset.filter(shared_status='ALL', is_published=True).select_related(
            'published_by').prefetch_related('categories')

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        exercises = context.get('training')
        categories = Categories.objects.all()
        results = len(exercises) if exercises else None
        title = 'Exercícios Publicados'

        # paginação
        page_obj, pagination_range = make_pagination(
            self.request, exercises, PER_PAGE
        )

        context.update(
            get_home_page_base_context(self.request, is_home_page=True)
        )

        context.update({
            'exercises': page_obj,
            'categories': categories,
            'results_count': results,
            'pagination_range': pagination_range,
            'title': title,
            'page_tag': title,
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
                Q(title__icontains=self.search_term) |
                Q(categories__name__icontains=self.search_term) |
                Q(published_by__username__icontains=self.search_term)
            ),
            shared_status='ALL', is_published=True
        ).distinct()

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        title = f'Exercícios Publicados > Busca > "{self.search_term}"'

        context.update({
            'title': title,
            'page_tag': title,
            'additional_url_query': f'&q={self.search_term}',
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
            shared_status='ALL',
            is_published=True,
        )

        if not queryset:
            self.category = Categories.objects.filter(
                pk=self.kwargs.get('id')
            ).first()

        return queryset

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        # filtrando no banco para obter no nome da categoria com base no id
        try:
            category_name = context.get('training', '')[0].categories.filter(
                id=self.kwargs.get('id')
            ).first()
        except IndexError:
            category_name = self.category.name if self.category else None

        if category_name is None:
            raise Http404()

        title = f'Exercícios Publicados > {category_name}'

        context.update({
            'title': title,
            'page_tag': title,
            'is_filtered': True,
        })

        return context


class ExerciseDetailClassView(DetailView):
    template_name = 'training/pages/exercise_detail.html'
    model = Exercises
    context_object_name = 'exercise_detail'
    slug_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(shared_status='ALL', is_published=True).select_related(
            'published_by'
        ).prefetch_related('categories')

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        exercise = context.get('exercise_detail')

        context.update(get_home_page_base_context(
            self.request, is_detail_page=True
        ))

        http_referer = self.request.META.get('HTTP_REFERER')

        url_to_redirect = http_referer if http_referer is not None else reverse(
            'training:home'
        )

        context.update({
            'exercise': exercise,
            'title': f'{exercise}',
            'page_tag': f'{exercise}',
            'url_to_redirect': url_to_redirect
        })

        return context


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
# classe para Página de explicação da api
class ApiExplanationClassView(View):
    def get(self, *args, **kwargs):
        title = 'NattyorNot - API'

        api_media_images = ApiMediaImages.objects.all()

        api_media_dict = {
            'access_token': api_media_images[0].image,
            'auth': api_media_images[1].image,
            'post': api_media_images[2].image,
        }

        exercises_json_dumped = json.dumps(
            exercises_json, indent=1, ensure_ascii=False
        )

        context = get_home_page_base_context(self.request)

        context.update({
            'title': title,
            'page_tag': title,
            'exercises_json': exercises_json_dumped,
            'api_images': api_media_dict,
        })

        return render(
            self.request, 'training/pages/nattyornot_api.html', context=context
        )
