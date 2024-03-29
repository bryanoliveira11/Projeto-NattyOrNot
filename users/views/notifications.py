from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.decorators import method_decorator
from django.views.generic import View

from users.models import UserNotifications, UserProfile


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

    def is_valid_user(self):
        user = self.request.user.get_username()
        if self.request.POST.get('username') != user:
            return False
        return True

    def get_previous_page_url(self):
        try:
            # urls de search do site
            search_urls_dict = {
                f'{reverse('training:search')}': reverse('training:home'),
                f'{reverse('dashboard:user_dashboard_search')}': reverse(
                    'dashboard:user_dashboard'
                ),
                f'{reverse('users:user_workouts_search')}': reverse(
                    'users:user_workouts'
                ),
            }

            path = self.request.POST.get('previous_page')
            previous_page = path if path else reverse('training:home')

            # usuário apagou uma notificação na url de search
            search_path = search_urls_dict.get(previous_page)

            if search_path is not None:
                previous_page = search_path

            return redirect(previous_page)

        except NoReverseMatch:
            return redirect(reverse('training:home'))

    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        notifications = UserNotifications.objects.filter(
            send_to=self.request.user,
        )

        if not self.is_valid_user():
            messages.error(self.request, 'Erro ao Deletar Notificação.')
            return self.get_previous_page_url()

        if notifications:
            notifications.delete()
            self.adjust_notifications_value(set_to_zero=True)

        return self.get_previous_page_url()


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserNotificationDeleteSingle(UserNotificationsDeleteClassView):
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        notification = UserNotifications.objects.filter(
            pk=self.kwargs.get('id'), send_to=self.request.user
        ).first()

        if not self.is_valid_user() or not notification:
            messages.error(self.request, 'Erro ao Deletar Notificação.')
            return self.get_previous_page_url()

        if notification:
            notification.delete()
            self.adjust_notifications_value(minus_one=True)

        return self.get_previous_page_url()
