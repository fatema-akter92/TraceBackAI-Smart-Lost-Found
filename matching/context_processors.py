from .models import MatchNotification


def notification_counts(request):
    if request.user.is_authenticated:
        unread_count = MatchNotification.objects.filter(recipient=request.user, is_read=False).count()
        recent_notifications = MatchNotification.objects.filter(recipient=request.user)[:5]
        return {
            'unread_notifications_count': unread_count,
            'recent_notifications': recent_notifications,
        }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
    }
