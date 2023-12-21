from unittest.mock import patch

from django.urls import resolve, reverse

from training import views

from .test_base import ExercisesTestBaseClass


class TrainingHomePageTest(ExercisesTestBaseClass):
    def test_training_home_view_function_is_correct(self):
        view = resolve(reverse('training:home'))
        self.assertIs(view.func.view_class, views.HomeClassView)

    def test_training_home_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('training:home'))
        self.assertEqual(response.status_code, 200)

    def test_training_home_template_shows_right_message_if_no_exercises(self):
        response = self.client.get(reverse('training:home'))
        self.assertIn(
            'Parece que não há exercícios, não é mesmo ?',
            response.content.decode('utf-8')
        )

    def test_training_home_view_loads_correct_template(self):
        response = self.client.get(reverse('training:home'))
        self.assertTemplateUsed(response, 'training/pages/home.html')

    def test_training_home_template_loads_exercises(self):
        # need a exercise for this test
        self.make_exercise()
        response = self.client.get(reverse('training:home'))
        content = response.content.decode('utf-8')
        training_context = response.context['training']
        self.assertIn('Test Exercise Title', content)
        self.assertEqual(len(training_context), 1)

    def test_training_home_template_dont_load_exercises_not_published(self):
        ''' Test if is_published False exercises are not showing  '''
        self.make_exercise(is_published=False)
        response = self.client.get(reverse('training:home'))
        self.assertIn(
            'Parece que não há exercícios, não é mesmo ?',
            response.content.decode('utf-8')
        )

    def test_exercise_home_is_paginated(self):
        self.make_multiple_exercises(number_to_make=2)

        with patch('training.views.exercises.PER_PAGE', new=1):
            response = self.client.get(reverse('training:home'))
            exercises = response.context['exercises']
            paginator = exercises.paginator

        # should have 2 pages in
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 1)
        self.assertEqual(len(paginator.get_page(2)), 1)

    def test_invalid_page_query_uses_page_one(self):
        self.make_multiple_exercises(number_to_make=2)

        with patch('training.views.exercises.PER_PAGE', new=1):
            response = self.client.get(reverse('training:home') + '?page=1A')
            self.assertEqual(1, response.context['exercises'].number)
