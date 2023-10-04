from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from training.models import Categories, Exercises
from training.permissions import IsOwner
from training.serializers import CategoriesSerializer, ExercisesSerializer


class ExercisesApiV1Pagination(PageNumberPagination):
    page_size = 10


# api para exercícios
class ExercisesApiV1ViewSet(ModelViewSet):
    queryset = Exercises.objects.filter(
        is_published=True).order_by('-id').select_related(
            'published_by').prefetch_related('categories')
    serializer_class = ExercisesSerializer
    pagination_class = ExercisesApiV1Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'options', 'head', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):  # post
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(published_by=request.user)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.request.query_params.get(  # type:ignore
            'category_id', ''
        )
        if category_id != '' and category_id.isnumeric():
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_object(self):
        id = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(),]

        return super().get_permissions()


# api para categorias
class CategoryApiV1ViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = ExercisesApiV1Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'options', 'head', 'post', 'patch']


# detalhes das categorias
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
