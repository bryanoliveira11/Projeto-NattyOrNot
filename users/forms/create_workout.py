from django import forms
from django_select2 import forms as s2forms

from dashboard.forms.create_exercise import CreateFormMixin
from training.models import Exercises
from users.models import UserWorkouts
from utils.django_forms import add_attr, add_placeholder


class ExercisesS2MultipleWidget(s2forms.ModelSelect2MultipleWidget):
    def label_from_instance(self, obj: Exercises):
        return f'{obj.title} - {obj.published_by}'

    def result_from_instance(self, obj: Exercises, request):
        return {
            'id': obj.pk,
            'text': self.label_from_instance(obj),
            'cover': obj.cover.url,
        }


class CreateWorkoutForm(forms.ModelForm, CreateFormMixin):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['title'], 'Digite o Nome do Treino')
        add_attr(self.fields['title'], 'class', 'span-2')
        add_attr(self.fields['exercises'], 'class', 'span-2')
        add_attr(self.fields['shared_status'], 'class', 'span-2')
        add_attr(self.fields['shared_status'], 'class', 'single-select')

    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercises.objects.filter(
            is_published=True, shared_status='ALL'
        ).order_by('-pk'),
        label='Exercícios Disponíveis',
        widget=ExercisesS2MultipleWidget(
            model=Exercises,
            queryset=Exercises.objects.filter(
                is_published=True, shared_status='ALL'
            ).order_by('-pk'),
            search_fields=[
                'title__icontains',
                'categories__name__icontains',
                'published_by__username__icontains',
            ],
            max_results=10,
            attrs={
                'data-placeholder': 'Buscar por Nome, Categoria ou Usuário',
                'selectionCssClass': 'form-control',
                'data-minimum-input-length': 2,
                'data-close-on-select': 'false',
                'data-language': 'pt-BR',
            },
        )
    )

    shared_status = forms.ChoiceField(
        choices=UserWorkouts._meta.get_field('shared_status').choices,
        label='Visibilidade',
        required=True,
        help_text='''
        Compartilhe Exercícios com Outros Usuários.
        '''
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
            'title', 'exercises', 'shared_status',
        ]

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        self.validate_google_recaptcha(
            data=self.data, add_error=self.add_error)
        return super_clean
