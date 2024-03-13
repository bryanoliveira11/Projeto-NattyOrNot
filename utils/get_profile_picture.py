from users.models import UserProfile


def get_profile_picture(request, user):
    try:
        user_profile = UserProfile.objects.filter(user=user).first()

        if not user_profile:
            return

        user_picture = user_profile.profile_picture.url

        if not user_picture:
            return

        request.session['user_picture'] = user_picture

    except ValueError:
        ...
