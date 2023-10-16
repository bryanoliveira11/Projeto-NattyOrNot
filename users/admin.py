from django.contrib import admin

from users.models import UserProfile, UserWorkouts


@admin.register(UserProfile)
class AdminUser(admin.ModelAdmin):
    list_display = 'user', 'profile_picture',
    list_display_links = 'user',
    search_fields = 'id', 'user',
    ordering = '-id',
    list_filter = 'user',
    list_per_page = 10


@admin.register(UserWorkouts)
class AdminUserWorkouts(admin.ModelAdmin):
    list_display = 'id', 'title', 'exercises_total', 'user', 'created_at'
    list_display_links = 'id', 'title',
    search_fields = 'id', 'title', 'user',
    ordering = '-id',
    list_filter = 'user', 'created_at',
    list_per_page = 10
