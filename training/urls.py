from django.urls import path

from training import views

app_name = 'training'

urlpatterns = [
    path('', views.HomeClassView.as_view(), name='home'),
    path('exercises/search/', views.SearchClassView.as_view(), name='search'),
    path(
        'exercises/category/<int:id>/',
        views.CategoriesFilterClassView.as_view(),
        name='category'
    ),
    path
    ('exercises/detail/<slug:slug>/',
     views.ExerciseDetailClassView.as_view(), name='exercises_detail'
     ),
]
