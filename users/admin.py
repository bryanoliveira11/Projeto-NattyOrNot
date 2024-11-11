from django.contrib import admin

from users.models import UserFollows, UserHealth, UserProfile, UserWorkouts


@admin.register(UserProfile)
class AdminUser(admin.ModelAdmin):
    list_display = 'user', 'profile_picture', \
        'created_at', 'updated_at',
    list_display_links = 'user',
    search_fields = 'id', 'user',
    ordering = '-id',
    list_filter = 'user',
    list_per_page = 10


@admin.register(UserWorkouts)
class AdminUserWorkouts(admin.ModelAdmin):
    list_display = 'id', 'title', 'exercises_total', 'user', \
        'created_at', 'updated_at', 'shared_status',
    list_display_links = 'id', 'title',
    list_editable = 'shared_status',
    search_fields = 'id', 'title', 'user', 'shared_status',
    ordering = '-id',
    list_filter = 'user', 'created_at', 'shared_status',
    list_per_page = 10


@admin.register(UserHealth)
class AdminUserHealth(admin.ModelAdmin):
    list_display = 'id', 'user', 'height', 'weight', 'imc', \
        'protein_intake', 'water_intake', 'updated_at',
    list_display_links = 'id', 'user',
    search_fields = 'id', 'title', 'height', 'weight', 'imc',
    ordering = '-id',
    list_filter = 'user', 'height', 'weight', 'imc',
    list_per_page = 10


@admin.register(UserFollows)
class AdminUserFollows(admin.ModelAdmin):
    list_display = 'id', 'follower', 'following',
    list_display_links = 'id', 'follower',
    ordering = '-id',
    list_per_page = 10
