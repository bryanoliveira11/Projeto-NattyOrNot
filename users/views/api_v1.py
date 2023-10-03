from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.serializers import UserSerializer


class UserApiV1Pagination(PageNumberPagination):
    page_size = 10


class UserApiV1ViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    pagination_class = UserApiV1Pagination
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        User = get_user_model()
        queryset = User.objects.filter(
            username=self.request.user.username  # type:ignore
        )
        return queryset

    @action(
        methods=['get'],
        detail=False
    )
    def me(self, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data)
