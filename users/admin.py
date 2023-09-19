from django.contrib import admin

from users.models import UserProfile


@admin.register(UserProfile)
class AdminUser(admin.ModelAdmin):
    list_display = 'user', 'profile_picture',
