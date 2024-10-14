"""
URL configuration for NattyOrNot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.socialaccount.providers.google import views as all_auth_views
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.views.all_auth import login_cancelled

handler404 = 'training.views.error404.error_404'

urlpatterns = [
    path('', include('training.urls')),
    path('select2/', include('django_select2.urls')),
    path('user/', include('users.urls')),
    path(
        'accounts/social/login/cancelled/',
        login_cancelled,
        name='socialaccount_login_cancelled'
    ),
    path(
        'accounts/google/login/callback/',
        all_auth_views.oauth2_callback,
        name='google_callback'
    ),
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include("debug_toolbar.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
