from django.db import models
from users.models import User
from vehicles.models import Vehicle
from django.utils import timezone



class PCN(models.Model):
    ticket_type = models.CharField(max_length =300)
    pcn = models.TextField()
    date_of_notice = models.DateField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    front_ticket_image = models.ImageField(upload_to="front_ticket_image/")
    back_ticket_image = models.ImageField(upload_to="back_ticket_image/")
    is_paid = models.BooleanField(default=False)
    is_denied = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)

    
    class Meta:
        ordering =("-id",)
    