from django.shortcuts import render

from utils.get_notifications import get_notifications


def error_404(request, exception):
    notifications, notifications_total = get_notifications(request)

    return render(
        request,
        'global/partials/error404.html',
        context={
            'title': 'Erro 404',
            'notifications': notifications,
            'notification_total': notifications_total,
        },
        status=404
    )
