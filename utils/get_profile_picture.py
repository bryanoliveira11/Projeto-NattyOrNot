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


# função para pegar as fotos dos usuários que postaram algo na home page
def get_users_profile_pictures_by_exercises(exercises: list):
    user_list = [
        exercise.published_by for exercise in
        exercises if exercise.published_by
    ]
    user_profiles = UserProfile.objects.filter(
        user__in=user_list
    ).select_related('user')

    users_data = {
        profile.user: f'media/{profile.profile_picture}'
        for profile in user_profiles
    }

    return users_data
