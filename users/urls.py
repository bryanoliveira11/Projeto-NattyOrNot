from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'users'

user_api_v1_router = SimpleRouter()
user_api_v1_router.register(
    'users/api/v1', views.UserApiV1ViewSet, basename='users-api'
)

urlpatterns = [
    # user /
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    # user profile urls
    path(
        '<str:username>/profile/',
        views.UserProfileDetailClassView.as_view(),
        name='user_profile'
    ),
    path(
        '<str:username>/profile/change/password/',
        views.UserProfileChangePassword.as_view(),
        name='user_profile_change_password'
    ),
    # notifications delete path
    path(
        'notification/<int:id>/delete/',
        views.UserNotificationDeleteSingle.as_view(),
        name='notification_delete_single'
    ),
    path(
        'notifications/delete/',
        views.UserNotificationsDeleteClassView.as_view(),
        name='notifications_delete'
    ),
    # user workouts urls
    path(
        'workouts/',
        views.UserWorkoutsPageClassView.as_view(),
        name='user_workouts'
    ),
    path(
        'workouts/search/',
        views.UserWorkoutsPageSearchClassView.as_view(),
        name='user_workouts_search'
    ),
    path(
        'workout/<int:id>/detail/',
        views.UserWorkoutsPageDetailClassView.as_view(),
        name='user_workout_detail'
    ),
    path(
        'workout/create/',
        views.UserWorkoutClassView.as_view(),
        name='user_workout_create'
    ),
    path(
        'workout/<int:id>/edit/',
        views.UserWorkoutClassView.as_view(),
        name='user_workout_edit'
    ),
    # delete workout
    path(
        'workout/<int:id>/delete/',
        views.UserWorkoutDeleteClassView.as_view(),
        name='user_workout_delete'
    ),
    # share workout
    path(
        'workout/<int:id>/share/',
        views.UserWorkoutShareClassView.as_view(),
        name='user_workout_share'
    ),
    path(
        'workout/<int:id>/unshare/',
        views.UserWorkoutUnshareClassView.as_view(),
        name='user_workout_unshare'
    ),
    # workout filters
    path(
        'workouts/is_shared=<str:is_shared>/',
        views.UserWorkoutsIsSharedFilterClassView.as_view(),
        name='user_workout_is_shared'
    ),
    # user dashboard urls
    path(
        'dashboard/exercises/',
        views.DashboardUserClassView.as_view(),
        name='user_dashboard'
    ),
    path(
        'dashboard/exercises/search/',
        views.DashboardSearchClassView.as_view(),
        name='user_dashboard_search'
    ),
    path(
        'dashboard/exercises/shared=<str:shared_status>/',
        views.DashboardSharedStatusFilterClassView.as_view(),
        name='user_dashboard_shared_filter'
    ),
    path(
        'dashboard/exercises/category/<int:id>/',
        views.DashboardUserCategoryClassView.as_view(),
        name='user_dashboard_category'
    ),
    # delete exercise
    path(
        'dashboard/exercise/<int:id>/delete/',
        views.UserExerciseDeleteClassView.as_view(),
        name='user_exercise_delete'
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
