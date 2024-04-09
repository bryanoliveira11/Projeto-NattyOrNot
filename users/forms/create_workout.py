from django import forms

from dashboard.forms.create_exercise import CreateFormMixin
from training.models import Exercises
from users.models import UserWorkouts
from utils.django_forms import add_attr, add_placeholder


class CreateWorkoutForm(forms.ModelForm, CreateFormMixin):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['title'], 'Digite o Nome do Treino')
        add_attr(self.fields['title'], 'class', 'span-2')
        add_attr(self.fields['exercises'], 'class', 'span-2')
        add_attr(self.fields['exercises'], 'class', 'multiple-select')

    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercises.objects.filter(
            is_published=True, shared_status='ALL'
        ).order_by('-pk'),
        label='Exercícios Disponíveis',
        help_text='''Se estiver em um Computador segure a tecla CTRL
          para selecionar mais de um Exercício.''',
    )

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

    class Meta:
        model = UserWorkouts
        fields = [
            'title',
        ]

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        self.validate_google_recaptcha(
            data=self.data, add_error=self.add_error)
        return super_clean
