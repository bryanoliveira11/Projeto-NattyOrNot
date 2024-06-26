from django.template import Library

from utils import filters

register = Library()


@register.filter
def username_limit_length(username):
    return filters.username_limit_length(username)


@register.filter
def title_limit_length(title: str):
    return filters.title_limit_length(title)


@register.filter
def format_series(series):
    return filters.format_series(series)


@register.filter
def format_reps(reps):
    return filters.format_reps(reps)


@register.filter
def format_exercises_num(value):
    return filters.format_exercises_num(value)


@register.filter
def format_favorites_text(value):
    return filters.format_favorites_text(value)
