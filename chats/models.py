from django.db import models
from django.utils import timezone
from users.models import User

class Chat(models.Model):
    message = models.TextField()
    ##This will be true when the user sends it
    sent = models.BooleanField(default=True)
    date_sent = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.message
    
