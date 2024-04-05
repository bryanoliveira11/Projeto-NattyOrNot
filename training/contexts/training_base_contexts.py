from django.urls import reverse

from utils.get_notifications import get_notifications
from utils.get_profile_picture import get_users_profile_pictures_by_exercises


def get_home_page_base_context(
    request, exercises=[], is_home_page=False, is_detail_page=False
):
    notifications, notifications_total = get_notifications(request)
    users_data = get_users_profile_pictures_by_exercises(exercises)

    return {
        'users_data': users_data,
        'notifications': notifications,
        'notification_total': notifications_total,
        'search_form_action': reverse('training:search'),
        'placeholder': 'Pesquisar na Home',
        'is_home_page': is_home_page,
        'is_detail_page': is_detail_page
    }
