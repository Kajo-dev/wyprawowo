# utils.py
from .models import Notification

def create_notification(user, message, notification_created_by):
    Notification.objects.create(user=user, message=message, notification_created_by=notification_created_by)