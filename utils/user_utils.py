from django.contrib.auth import get_user_model

from users.models import UserFollows

User = get_user_model()


def get_user_follow_stats(user_id):
    user = User.objects.filter(pk=user_id).first()

    if not user:
        return

    follower_count = UserFollows.objects.filter(following=user).count()
    following_count = UserFollows.objects.filter(follower=user).count()

    return follower_count, following_count
