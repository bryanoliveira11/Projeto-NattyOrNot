from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve, reverse


def lockout(request, credentials, *args, **kwargs):
    messages.error(
        request, 'Limite Máximo de Tentativas Excedido Para Esse Usuário. '
        'Tente Novamente em 15 Minutos.'
    )
    app_namespace = resolve(request.path).namespace
    url_name = resolve(request.path).url_name
    return redirect(reverse(f'{app_namespace}:{url_name}'))
