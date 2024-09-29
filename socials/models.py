from django.db import models
from user_manager.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'Notification for {self.user.email}: {self.message}'