from django.utils.text import slugify
from rest_framework import serializers

from training.models import Categories, Exercises
from training.validators import ExerciseValidator
from utils.strings import generate_random_string


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
        view_name='training:api_v1_category',
        read_only=True,
    )

    def validate(self, attrs):
        if self.instance is not None and attrs.get('series') is None:
            attrs['series'] = self.instance.series

        if self.instance is not None and attrs.get('reps') is None:
            attrs['reps'] = self.instance.reps

        if self.instance is not None and attrs.get('slug') is None:
            try:
                attrs['slug'] = slugify(
                    attrs['title'] + generate_random_string(5))
            except KeyError:
                ...

        super_validate = super().validate(attrs)
        ExerciseValidator(data=attrs, ErrorClass=serializers.ValidationError)
        return super_validate

    def save(self, **kwargs):
        return super().save(**kwargs)
