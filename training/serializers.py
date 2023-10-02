from rest_framework import serializers

from training.models import Categories, Exercises


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name']


class ExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = [
            'id', 'title', 'description', 'slug', 'series',
            'reps', 'categories', 'category_names', 'category_links',
            'public', 'published_by', 'user', 'cover'
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)

    user = serializers.StringRelatedField(
        read_only=True, source='published_by'
    )

    category_names = CategoriesSerializer(
        many=True, source='categories', read_only=True
    )

    category_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='categories',
        lookup_field='id',
        view_name='training:exercises_api_v1_category',
        read_only=True,
    )

    def save(self, **kwargs):
        return super().save(**kwargs)
