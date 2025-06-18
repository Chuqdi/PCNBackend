from django.db import models
from django.utils import timezone
from users.models import User




class Appeal(models.Model):
    pcn = models.CharField(max_length=50)
    registeration_number = models.CharField(max_length=50)
    date_of_notice = models.DateField()
    status = models.TextField(null=True, blank=True)
    ticket_type = models.CharField(max_length=50)
    front_ticket_image = models.ImageField(upload_to="front_ticket_image/")
    back_ticket_image = models.ImageField(upload_to="back_ticket_image/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return super().__str__()