from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # user dashboard urls
    path(
        'exercises/',
        views.DashboardUserClassView.as_view(),
        name='user_dashboard'
    ),
    path(
        'exercises/search/',
        views.DashboardSearchClassView.as_view(),
        name='user_dashboard_search'
    ),
    path(
        'exercises/shared=<str:shared_status>/',
        views.DashboardSharedStatusFilterClassView.as_view(),
        name='user_dashboard_shared_filter'
    ),
    path(
        'exercises/category/<int:id>/',
        views.DashboardUserCategoryClassView.as_view(),
        name='user_dashboard_category'
    ),
    # delete exercise
    path(
        'exercise/<int:id>/delete/',
        views.DashboardDeleteExerciseClassView.as_view(),
        name='user_exercise_delete'
    ),
    path(
        'exercise/create/',
        views.DashboardExerciseClassView.as_view(),
        name='create_exercise'
    ),
    path(
        'exercise/<int:id>/edit/',
        views.DashboardExerciseClassView.as_view(),
        name='edit_exercise'
    ),
]
