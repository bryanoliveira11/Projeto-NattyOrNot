from django.contrib import admin

from .models import ApiMediaImages, Categories, Exercises


@admin.register(Exercises)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'published_by', 'created_at', 'updated_at', 'is_published', 'shared_status',
    list_display_links = 'id', 'title',
    list_editable = 'is_published', 'shared_status',
    search_fields = 'id', 'title', 'description'
    list_filter = 'published_by', 'categories', 'created_at', 'updated_at', 'is_published', 'shared_status',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_per_page = 10
    filter_horizontal = ('categories', )


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    ordering = '-id',
    search_fields = 'id', 'name',
    list_per_page = 10


@admin.register(ApiMediaImages)
class ApiMediaAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    ordering = '-id',
    search_fields = 'id', 'name',
    list_per_page = 5
