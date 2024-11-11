from os import environ

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from base_templates.emails.email_templates import followed_by
from users.email_service import send_html_mail
from users.models import UserFollows, UserNotifications, UserProfile
from utils.get_notifications import get_notifications
from utils.pagination import make_pagination

User = get_user_model()
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', '')


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserFollowsClassView(View):
    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        follower = self.request.user
        following = get_object_or_404(User, pk=self.kwargs.get('id'))

        if follower == following:
            return redirect(
                reverse('users:user_profile', args=(following.username,))
            )

        if UserFollows.objects.filter(
            follower=follower, following=following
        ).exists():
            return redirect(
                reverse('users:user_profile', args=(following.username,))
            )

        UserFollows.objects.create(
            follower=follower,
            following=following,
        )

        url = reverse('users:user_profile', args=(follower,))

        UserNotifications.objects.create(
            subject='Novo Seguidor',
            subject_html='Novo Seguidor',
            message=f'<a class="notification-url" href="{
                url}">"{follower}"</a> '
            'começou a seguir você.',
            send_by='NattyOrNot',
            send_to=following,
        )

        send_html_mail(
            subject='Novo Seguidor',
            html_content=followed_by(str(follower)),
            sender=EMAIL_HOST_USER,
            recipient_list=[following.email],
            dev_mode=False,
        )

        return redirect(
            reverse('users:user_profile', args=(following.username,))
        )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserUnfollowsClassView(View):
    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        follower = self.request.user
        following = get_object_or_404(User, pk=self.kwargs.get('id'))

        if follower == following:
            return redirect(
                reverse('users:user_profile', args=(following.username,))
            )

        user_follow = UserFollows.objects.filter(
            follower=follower, following=following
        ).first()

        if user_follow:
            user_follow.delete()

        return redirect(
            reverse('users:user_profile', args=(following.username,))
        )


class UserFollowers(View):
    def get_followers(self, user_instance):
        followers_ids = UserFollows.objects.filter(
            following=user_instance
        ).values_list('follower', flat=True)
        return UserProfile.objects.filter(
            user_id__in=followers_ids
        ).select_related('user').order_by('-pk')

    def get(self, *args, **kwargs):
        username = self.kwargs.get('username')
        followers = None
        page_obj = None
        pagination_range = None

        if not username:
            raise Http404()

        user_instance = User.objects.filter(username=username).first()

        if user_instance:
            followers = self.get_followers(user_instance)

        notifications, notifications_total = get_notifications(self.request)

        if followers is not None:
            page_obj, pagination_range = make_pagination(
                self.request, followers, 10
            )

        return render(self.request, 'users/pages/followers.html', context={
            'followers': page_obj,
            'exercises': page_obj,
            'pagination_range': pagination_range,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': f'Seguidores de {user_instance}',
        })


class UserFollowing(View):
    def get_following(self, user_instance):
        following_ids = UserFollows.objects.filter(
            follower=user_instance
        ).values_list('following', flat=True)
        return UserProfile.objects.filter(
            user_id__in=following_ids
        ).select_related('user').order_by('-pk')

    def get(self, *args, **kwargs):
        username = self.kwargs.get('username')
        following = None
        page_obj = None
        pagination_range = None

        if not username:
            raise Http404()

        user_instance = User.objects.filter(username=username).first()

        if user_instance:
            following = self.get_following(user_instance)

        notifications, notifications_total = get_notifications(self.request)

        if following is not None:
            page_obj, pagination_range = make_pagination(
                self.request, following, 10
            )

        return render(self.request, 'users/pages/following.html', context={
            'following': page_obj,
            'exercises': page_obj,
            'pagination_range': pagination_range,
            'notifications': notifications,
            'notification_total': notifications_total,
            'title': f'Seguidos por {user_instance}',
        })
