from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from users.models import UserNotifications, UserProfile
from utils.get_notifications import get_notifications


class UserNotificationsDeleteClassView(View):
    def adjust_notifications_value(self, set_to_zero=False, minus_one=False):
        user_profile = UserProfile.objects.filter(
            user_id=self.request.user
        ).first()

        if user_profile:
            if set_to_zero:
                user_profile.notifications_total = 0
                user_profile.save()

            if minus_one:
                user_profile.notifications_total -= 1
                user_profile.save()

    def validate_user(self):
        if self.request.POST.get('username') != self.request.user.username:  # type:ignore
            messages.error(self.request, 'Usuário Inválido.')
            return redirect(reverse('training:home'))

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

        self.validate_user()

        if notifications:
            notifications.delete()
            self.adjust_notifications_value(set_to_zero=True)

        previous_page = self.request.POST.get(
            'previous_page', reverse('training:home')
        )
        return redirect(previous_page)


class UserNotificationDeleteSingle(UserNotificationsDeleteClassView):
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        notification = UserNotifications.objects.filter(
            pk=self.kwargs.get('id')
        ).first()

        self.validate_user()

        if notification:
            notification.delete()
            self.adjust_notifications_value(minus_one=True)

        previous_page = self.request.POST.get(
            'previous_page', reverse('training:home')
        )
        return redirect(previous_page)
