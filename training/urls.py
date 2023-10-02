from django.urls import include, path
from rest_framework.routers import SimpleRouter

from training import views

app_name = 'training'

# router
exercise_api_v1_router = SimpleRouter()
exercise_api_v1_router.register(
    'exercises/api/v1', views.ExercisesApiV1ViewSet, basename='exercises-api'
)

urlpatterns = [
    path('', views.HomeClassView.as_view(), name='home'),
    path('exercises/search/', views.SearchClassView.as_view(), name='search'),
    path(
        'exercises/category/<int:id>/',
        views.CategoriesFilterClassView.as_view(),
        name='category'
    ),
    path(
        'exercises/detail/<slug:slug>/',
        views.ExerciseDetailClassView.as_view(),
        name='exercises_detail'
    ),
    # api paths
    path(
        'exercises/api/v1/category/<int:id>/',
        views.CategoryApiV1Detail.as_view(),
        name='exercises_api_v1_category'
    ),
    path('', include(exercise_api_v1_router.urls)),
]
