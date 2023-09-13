from django.template import Library

from utils import filters

register = Library()


@register.filter
def username_limit_length(username):
    return filters.username_limit_length(username)
