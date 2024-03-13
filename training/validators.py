from collections import defaultdict

from django.core.exceptions import ValidationError

from utils.django_forms import is_positive_number


# essa classe é responsável por validar o form para os exercícios
class ExerciseValidator:
    def __init__(
        self, data, errors=None, ErrorClass=None, isApi=False
    ) -> None:
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.isApi = isApi
        self.clean()

    def validate_min_length(self, field_name, field_value, min_length):
        if field_value:
            if len(field_value) < min_length:
                error_message = f'Digite ao menos {min_length} Caracteres.'
                self.errors[field_name].append(error_message)

    def clean(self, *args, **kwargs):
        cleaned_data = self.data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        series = cleaned_data.get('series')
        reps = cleaned_data.get('reps')
        categories = cleaned_data.get('categories')

        # validando se a descrição não é igual ao titulo
        if title == description:
            self.errors['title'].append(
                'Não pode ser igual a Descrição.'
            )
            self.errors['description'].append(
                'Não pode ser igual ao Título.'
            )

        self.validate_min_length(  # validando tamanho do titulo
            field_name='title', field_value=title, min_length=5
        )

        self.validate_min_length(  # validando tamanho da descricao
            field_name='description', field_value=description, min_length=5
        )

        # validando números de reps e series
        if not is_positive_number(series):
            self.errors['series'].append(
                'Digite um número inteiro maior que zero.'
            )

        if not is_positive_number(reps):
            self.errors['reps'].append(
                'Digite um número inteiro maior que zero.'
            )

        # validando categorias
        if not categories and not self.isApi:
            self.errors['categories'].append(
                'Escolha ao menos uma categoria.'
            )

        if self.errors:
            raise self.ErrorClass(self.errors)
