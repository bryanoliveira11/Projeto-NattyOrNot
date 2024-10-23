from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from users.models import UserFollows

User = get_user_model()


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
