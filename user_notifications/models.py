from django.db import models
from users.models import User


class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    expire_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email
