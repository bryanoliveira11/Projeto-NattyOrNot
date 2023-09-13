from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path(
        'dashboard/<str:user>/exercises/',
        views.DashboardUserClassView.as_view(),
        name='user_dashboard'
    ),
    path(
        'dashboard/<str:user>/exercises/category/<int:id>/',
        views.DashboardUserCategoryClassView.as_view(),
        name='user_dashboard_category'
    ),
    path(
        'dashboard/<str:user>/exercises/delete/<int:id>/',
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
]
