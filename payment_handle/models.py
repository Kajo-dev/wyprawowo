from django.db import models
from user_manager.models import User

class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_success = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)