from django.contrib import admin

from users.models import UserNotifications, UserProfile, UserWorkouts


@admin.register(UserProfile)
class AdminUser(admin.ModelAdmin):
    list_display = 'user', 'profile_picture', 'created_at', 'updated_at',
    list_display_links = 'user',
    search_fields = 'id', 'user',
    ordering = '-id',
    list_filter = 'user',
    list_per_page = 10


@admin.register(UserWorkouts)
class AdminUserWorkouts(admin.ModelAdmin):
    list_display = 'id', 'title', 'exercises_total', 'user', 'created_at', 'updated_at', 'is_shared',
    list_display_links = 'id', 'title',
    list_editable = 'is_shared',
    search_fields = 'id', 'title', 'user', 'is_shared',
    ordering = '-id',
    list_filter = 'user', 'created_at', 'is_shared',
    list_per_page = 10


@admin.register(UserNotifications)
class AdminUserNotifications(admin.ModelAdmin):
    list_display = 'id', 'subject', 'send_by', 'send_to', 'send_at'
    list_display_links = 'id', 'subject',
    search_fields = 'id', 'subject', 'send_to',
    ordering = '-id',
    list_filter = 'send_to', 'send_at',
    list_per_page = 10
