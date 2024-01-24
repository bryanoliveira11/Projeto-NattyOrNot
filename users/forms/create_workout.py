from django import forms

from training.models import Exercises
from users.forms.create_exercise import CreateFormMixin
from users.models import UserWorkouts
from utils.django_forms import add_attr, add_placeholder


class CreateWorkoutForm(forms.ModelForm, CreateFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['title'], 'Digite o Nome do Treino')
        add_attr(self.fields['title'], 'class', 'span-2')
        add_attr(self.fields['exercises'], 'class', 'span-2')
        add_attr(self.fields['exercises'], 'class', 'select-more-height')

    captcha = forms.CharField(
        label='',
        required=False,
        widget=forms.HiddenInput(
            attrs={'class': 'span-2 center captcha-form'}
        ))

    title = forms.CharField(
        label='Título do Treino',
        required=True,
        max_length=155,
        min_length=5,
        error_messages={
            'required': 'Digite o Título.',
        }
    )

    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercises.objects.filter(is_published=True),
        label='Exercícios Publicados',
        help_text='Segure CTRL para selecionar mais de um exercício.',
    )

    class Meta:
        model = UserWorkouts
        fields = [
            'title',
            'exercises',
        ]

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        self.validate_google_recaptcha(
            data=self.data, add_error=self.add_error)
        return super_clean
