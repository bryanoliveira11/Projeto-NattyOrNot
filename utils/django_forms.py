import re

from django.core.exceptions import ValidationError


def add_attr(field, attr_name: str, attr_new_val: str):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val: str):
    add_attr(field, 'placeholder', f'{placeholder_val}'.strip())


def strong_password(password: str):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'Senha muito fraca.'
        )


def is_positive_number(field_number: int):
    if isinstance(field_number, int):
        if field_number > 0:
            return True
    return False


def is_positive_float_number(field_number: float):
    if isinstance(field_number, float):
        if field_number > 0:
            return True
    return False
