from django.utils.text import Truncator


def username_limit_length(username: str) -> str:
    if len(username) < 10:
        return 'Olá, ' + username
    return 'Bem-Vindo(a)'


def title_limit_length(title: str):
    if not len(title) >= 22:
        return title
    return str(Truncator(title).chars(19))


def format_series(series):
    if series > 1:
        return f'{series} Séries'

    return f'{series} Série'


def format_reps(reps):
    if reps > 1:
        return f'{reps} Repetições'

    return f'{reps} Repetição'
