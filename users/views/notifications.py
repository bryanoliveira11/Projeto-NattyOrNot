from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from users.models import UserNotifications, UserProfile
from utils.get_notifications import get_notifications


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
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

    def get_previous_page_url(self):
        # urls de search do site
        search_urls_dict = {
            f'{reverse('training:search')}': reverse('training:home'),
            f'{reverse('users:user_dashboard_search')}': reverse('users:user_dashboard'),
            f'{reverse('users:user_workouts_search')}': reverse('users:user_workouts'),
        }

        path = self.request.POST.get('previous_page')
        previous_page = path if path else reverse('training:home')

        # usuário apagou uma notificação na url de search
        search_path = search_urls_dict.get(previous_page)

        if search_path is not None:
            previous_page = search_path

        return previous_page

    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        notifications = UserNotifications.objects.filter(
            send_to=self.request.user,
        )

        self.validate_user()

        if notifications:
            notifications.delete()
            self.adjust_notifications_value(set_to_zero=True)

        return redirect(self.get_previous_page_url())


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
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

        return redirect(self.get_previous_page_url())
