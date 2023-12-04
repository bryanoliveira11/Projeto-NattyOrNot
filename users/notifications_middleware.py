from users.models import UserNotifications


# classe responsável por trazer as notificações do banco de dados
class NotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # buscar notificações:
        if request.user.is_authenticated:
            self.notifications = UserNotifications.objects.filter(
                send_to=request.user,
            ).order_by('-id')

            request.notifications = self.notifications
            request.notifications_total = len(self.notifications)
        else:
            request.notifications = []
            request.notifications_total = 0

        response = self.get_response(request)
        return response
