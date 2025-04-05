from .models import Startup, Notification

def user_startup(request):
    if request.user.is_authenticated:
        try:
            user_startup = Startup.objects.get(founder=request.user)
            return {'user_startup': user_startup}
        except Startup.DoesNotExist:
            return {'user_startup': None}
    return {'user_startup': None}

def notifications(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {
            'unread_notifications_count': unread_count
        }
    return {} 