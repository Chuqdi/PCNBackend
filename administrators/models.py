from django.db import models
from django.utils import timezone

class Admin(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    email = models.EmailField(unique=True)
    accepted = models.BooleanField(default=False)
    date_sent = models.DateTimeField(default=timezone.now)