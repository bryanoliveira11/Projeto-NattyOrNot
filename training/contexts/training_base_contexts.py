from django.urls import reverse

from utils.get_notifications import get_notifications


def get_home_page_base_context(request, is_home_page=False, is_detail_page=False):
    notifications, notifications_total = get_notifications(request)

    return {
        'notifications': notifications,
        'notification_total': notifications_total,
        'search_form_action': reverse('training:search'),
        'placeholder': 'Pesquise por um Exercício ou Categoria',
        'additional_search_placeholder': 'na Home',
        'is_home_page': is_home_page,
        'is_detail_page': is_detail_page
    }
