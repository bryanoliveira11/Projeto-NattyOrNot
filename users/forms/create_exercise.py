from os import environ

import requests
from django import forms
from django.core.exceptions import ValidationError

from training.models import Categories, Exercises
from training.validators import ExerciseValidator
from utils.django_forms import add_attr, add_placeholder


class CreateFormMixin:
    def validate_google_recaptcha(self, data, add_error):
        # google recaptcha
        recaptcha_response = data.get('g-recaptcha-response')

        if environ.get('RECAPTCHA_PRIVATE_KEY'):
            if not recaptcha_response:
                add_error(
                    'captcha', 'Marque a Caixa "Não sou um Robô".'
                )

        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': environ.get('RECAPTCHA_PRIVATE_KEY', ''),
                'response': recaptcha_response
            }
        )
        recaptcha_request.json()


class CreateExerciseForm(forms.ModelForm, CreateFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['title'], 'Digite o Título')
        add_placeholder(self.fields['description'], 'Digite a Descrição')
        add_placeholder(self.fields['series'], 'Digite o Número de Séries')
        add_placeholder(self.fields['reps'], 'Digite o Número de Repetições')
        add_attr(self.fields['title'], 'class', 'span-2')
        add_attr(self.fields['description'], 'class', 'span-2')
        add_attr(self.fields['categories'], 'class', 'span-2')
        add_attr(self.fields['categories'], 'class', 'multiple-select')
        add_attr(self.fields['shared_status'], 'class', 'span-2')
        add_attr(self.fields['shared_status'], 'class', 'single-select')

    title = forms.CharField(
        label='Título',
        required=True,
        max_length=155,
        error_messages={
            'required': 'Digite o Título.',
        }
    )

    series = forms.IntegerField(
        label='Número de Séries',
        required=True,
        error_messages={
            'required': 'Digite o número de séries.'
        }
    )

    reps = forms.IntegerField(
        label='Número de Repetições',
        required=True,
        error_messages={
            'required': 'Digite o número de repetições.'
        }
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
        label='Categorias',
        help_text='Dica : Segure a tecla CTRL para selecionar mais de uma categoria.',
    )

    shared_status = forms.ChoiceField(
        choices=Exercises._meta.get_field('shared_status').choices,
        label='Visibilidade',
        required=True,
        help_text='''
        Exercícios Compartilhados com Todos serão Validados antes de Serem Publicados.
        Além disso, não será Possível Edita-lo após a Aprovação.
        '''
    )

    cover = forms.FileField(
        label='Imagem / Gif',
        help_text='Dica : Um Gif ficará mais interessante do que uma imagem.',
        widget=forms.FileInput(
            attrs={
                'class': 'span-2',
            }
        ),
    )

    captcha = forms.CharField(
        label='',
        required=False,
        widget=forms.HiddenInput(
            attrs={'class': 'span-2 center mt'}
        ))

    class Meta:
        model = Exercises
        fields = [
            'title',
            'description',
            'series',
            'reps',
            'categories',
            'shared_status',
            'cover',
        ]

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        self.validate_google_recaptcha(
            data=self.data, add_error=self.add_error)
        ExerciseValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
