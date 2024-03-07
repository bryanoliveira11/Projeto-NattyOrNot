from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from training import views

app_name = 'training'

# router
exercise_api_v1_router = SimpleRouter()
exercise_api_v1_router.register(
    'exercises/api/v1', views.ExercisesApiV1ViewSet, basename='exercises-api'
)

urlpatterns = [
    path('', views.HomeClassView.as_view(), name='home'),
    path(
        '/nattyornot/api/',
        views.ApiExplanationClassView.as_view(),
        name='nattyornot_api'
    ),
    path('/exercises/search/', views.SearchClassView.as_view(), name='search'),
    path(
        '/exercises/category/<int:id>/',
        views.CategoriesFilterClassView.as_view(),
        name='category'
    ),
    path(
        '/exercises/detail/<slug:slug>/',
        views.ExerciseDetailClassView.as_view(),
        name='exercises_detail'
    ),
    # api paths
    path(
        '/exercises/api/v1/category/',
        views.CategoryApiV1ViewSet.as_view({'get': 'list'}),
        name='api_v1_categories'
    ),
    path(
        '/exercises/api/v1/category/<int:id>/',
        views.CategoryApiV1Detail.as_view(),
        name='api_v1_category'
    ),
    # token jwt paths
    path(
        '/exercises/api/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        '/exercises/api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        '/exercises/api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
    path('', include(exercise_api_v1_router.urls)),
]
