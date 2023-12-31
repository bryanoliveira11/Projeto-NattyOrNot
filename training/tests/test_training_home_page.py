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

    # home base context

    def test_training_home_has_right_context(self):
        response = self.client.get(reverse('training:home'))
        # title
        self.assertEqual(response.context['title'], 'Home')
        # page_tag
        self.assertEqual(response.context['page_tag'], 'Home - Exercícios')
        # search form action
        self.assertEqual(
            response.context['search_form_action'],
            reverse('training:search')
        )
        # search placeholder
        self.assertEqual(
            response.context['placeholder'],
            'Pesquise por um Exercício ou Categoria'
        )
        # search placeholder additional phrase
        self.assertEqual(
            response.context['additional_search_placeholder'], 'na Home'
        )
        # is home page ??? should be true
        self.assertEqual(
            response.context['is_home_page'], True
        )

    # search url context

    def test_training_home_search_url_has_right_context(self):
        search_term = 'test'
        response = self.client.get(
            reverse('training:search') + f'?q={search_term}'
        )
        self.assertEqual(
            response.context['title'], f'Busca por "{search_term}"'
        )
        self.assertEqual(
            response.context['page_tag'],
            f'Home - Resultados da Busca por "{search_term}"'
        )
        self.assertEqual(
            response.context['search_form_action'],
            reverse('training:search')
        )
        self.assertEqual(
            response.context['placeholder'],
            'Pesquise por um Exercício ou Categoria'
        )
        self.assertEqual(
            response.context['additional_search_placeholder'], 'na Home'
        )
        self.assertEqual(response.context['is_filtered'], True)

    # categories filter url context

    def test_training_home_categories_url_has_right_context(self):
        self.make_exercise()
        category_name = 'Test Category'
        response = self.client.get(reverse('training:category', args=(1,)))
        self.assertEqual(
            response.context['title'], f'Categoria - {category_name}'
        )
        self.assertEqual(
            response.context['page_tag'],
            f'Home - Filtrando por Exercícios de {category_name}'
        )
        self.assertEqual(
            response.context['search_form_action'],
            reverse('training:search')
        )
        self.assertEqual(
            response.context['placeholder'],
            'Pesquise por um Exercício ou Categoria'
        )
        self.assertEqual(
            response.context['additional_search_placeholder'], 'na Home'
        )
        self.assertEqual(response.context['is_filtered'], True)

    # detail page context

    def test_training_home_detail_url_has_right_context(self):
        exercise = self.make_exercise()
        response = self.client.get(
            reverse('training:exercises_detail', args=(exercise.slug,))
        )
        self.assertEqual(
            response.context['title'], f'{exercise.title}'
        )
        self.assertEqual(
            response.context['page_tag'],
            f'{exercise.title}'
        )
        self.assertEqual(
            response.context['search_form_action'],
            reverse('training:search')
        )
        self.assertEqual(
            response.context['placeholder'],
            'Pesquise por um Exercício ou Categoria'
        )
        self.assertEqual(
            response.context['additional_search_placeholder'], 'na Home'
        )
