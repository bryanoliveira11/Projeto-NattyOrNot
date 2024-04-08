from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from users.models import UserHealth
from utils.django_forms import (add_placeholder, is_positive_float_number,
                                is_positive_number)


class UserHealthForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_placeholder(self.fields['height'], 'EX.: 170')
        add_placeholder(self.fields['weight'], 'EX.: 70')

    height = forms.IntegerField(label='Sua Altura (cm)')
    weight = forms.FloatField(
        label=format_html(
            '<i class="fa-solid fa-weight-scale m-right"></i> Seu Peso (kg)'
        ),
    )

    class Meta:
        model = UserHealth
        fields = [
            'height',
            'weight',
        ]

    def clean(self, *args, **kwargs):
        height: int = self.cleaned_data.get('height', 0)
        weight: float = self.cleaned_data.get('weight', 0)

        if not is_positive_number(int(height)):
            self._my_errors['height'].append(
                'Digite um número inteiro maior que zero.'
            )

        if not is_positive_float_number(float(weight)):
            self._my_errors['weight'].append(
                'Digite um número maior que zero.'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super().clean(*args, **kwargs)
