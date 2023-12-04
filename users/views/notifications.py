from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from users.models import UserNotifications
from utils.get_notifications import get_notifications


class UserNotificationsDeleteClassView(View):
    def get(self, *args, **kwargs):
        notifications, notifications_total = get_notifications(self.request)

        return render(self.request, 'global/partials/error404.html', context={
            'notifications': notifications,
            'notification_total': notifications_total,
            'search_form_action': reverse('training:search'),
            'placeholder': 'Pesquise por um Exercício ou Categoria',
            'additional_search_placeholder': 'na Home',
            'title': 'Página Não Encontrada',
        })

    def post(self, *args, **kwargs):
        notifications = UserNotifications.objects.filter(
            send_to=self.request.user,
        )

        if self.request.POST.get('username') != self.request.user.username:  # type:ignore
            messages.error(self.request, 'Usuário Inválido.')
            return redirect(reverse('training:home'))

        notifications.delete()
        previous_page = self.request.POST.get(
            'previous_page', reverse('training:home')
        )
        return redirect(previous_page)
