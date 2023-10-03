from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'users'

user_api_v1_router = SimpleRouter()
user_api_v1_router.register(
    'users/api/v1', views.UserApiV1ViewSet, basename='users-api'
)

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path(
        'user/<str:username>/profile/',
        views.UserProfileDetailClassView.as_view(),
        name='user_profile'
    ),
    path(
        'dashboard/exercises/search/',
        views.DashboardSearchClassView.as_view(),
        name='user_dashboard_search'
    ),
    path(
        'dashboard/exercises/filter/is_published=<str:is_published>/',
        views.DashboardIsPublishedFilterClassView.as_view(),
        name='user_dashboard_is_published'
    ),
    path(
        'dashboard/exercises/',
        views.DashboardUserClassView.as_view(),
        name='user_dashboard'
    ),
    path(
        'dashboard/exercises/category/<int:id>/',
        views.DashboardUserCategoryClassView.as_view(),
        name='user_dashboard_category'
    ),
    path(
        'dashboard/exercise/<int:id>/delete/',
        views.DashboardDeleteExerciseClassView.as_view(),
        name='user_dashboard_delete'
    ),
    path(
        'dashboard/exercise/create/',
        views.DashboardExerciseClassView.as_view(),
        name='create_exercise'
    ),
    path(
        'dashboard/exercise/<int:id>/edit/',
        views.DashboardExerciseClassView.as_view(),
        name='edit_exercise'
    ),
    # api paths
    path('', include(user_api_v1_router.urls)),
]
