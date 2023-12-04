# traz as notificação salvas em request pelo middleware de notifications
# -> users > notification_middleware.py
def get_notifications(request):
    notifications = getattr(request, 'notifications', [])
    notifications_total = getattr(request, 'notifications_total', 0)

    return notifications, notifications_total
