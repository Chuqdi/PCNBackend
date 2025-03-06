from django.db import models
from users.models import User
from django.utils import timezone



class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    content = models.TextField()
    as_email = models.BooleanField(default=True)
    as_mobile_notification = models.BooleanField(default=True)
    date_sent = models.DateField(default=timezone.now)
    
    
    def __str__(self):
        return self.title