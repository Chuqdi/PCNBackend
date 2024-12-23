from django.db import models
from users.models import User

APP_SCREENS = [
        ("Home", 'Home'),
        ("Ticket", 'Ticket'),
        ("Plans", 'Plans')
    ]

class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    screen = models.TextField(
        choices=APP_SCREENS,
        null=True,
        blank=True
    )
    expire_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email
