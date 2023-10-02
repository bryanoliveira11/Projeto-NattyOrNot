from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from training.models import Categories, Exercises
from training.serializers import CategoriesSerializer, ExercisesSerializer


class ExercisesApiV1Pagination(PageNumberPagination):
    page_size = 10


class ExercisesApiV1ViewSet(ModelViewSet):
    queryset = Exercises.objects.filter(
        is_published=True
    ).order_by('-id').select_related('published_by').prefetch_related(
        'categories')
    serializer_class = ExercisesSerializer
    pagination_class = ExercisesApiV1Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'options', 'head', 'post', 'patch', 'delete']


class CategoryApiV1Detail(APIView):
    def get(self, request, **kwargs):
        category = get_object_or_404(Categories.objects.filter(
            pk=kwargs.get('id')
        ))
        serializer = CategoriesSerializer(
            instance=category,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data)
