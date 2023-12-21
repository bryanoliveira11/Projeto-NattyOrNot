from django.contrib.auth.models import User
from django.test import TestCase

from training.models import Categories, Exercises


class TrainingExercisesMixin:
    def make_category(self, name='Test Category'):
        Categories.objects.create(name=name)

    def make_user(
            self,
            first_name='Test',
            last_name='User',
            username='testuser',
            password='Senha123',
            email='test.user@gmail.com'):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_exercise(
            self,
            title='Test Exercise Title',
            description='E. Description',
            slug='test-ex-slug',
            series=3,
            reps=15,
            is_published=True,
            was_rejected=False,
            rejected=False,
            extra_info='',
            cover=None,
            user_data=None,):

        if user_data is None:
            user_data = {}

        exercise = Exercises.objects.create(
            title=title,
            description=description,
            slug=slug,
            series=series,
            reps=reps,
            is_published=is_published,
            was_rejected=was_rejected,
            rejected=rejected,
            extra_info=extra_info,
            cover=cover,
            published_by=self.make_user(**user_data),
        )

        category = self.make_category()

        if category:
            exercise.categories.set(category)

        return exercise

    def make_multiple_exercises(self, number_to_make=2):
        exercises = []

        for i in range(number_to_make):
            kwargs = {
                'title': f'Test Exercise Title {i}',
                'slug': f'test-ex-slug-{i}',
                'user_data': {'username': f'TestUserMultiple {i}'}
            }
            exercise = self.make_exercise(**kwargs)
            exercises.append(exercise)

        return exercises


class ExercisesTestBaseClass(TestCase, TrainingExercisesMixin):
    def setUp(self) -> None:
        return super().setUp()
