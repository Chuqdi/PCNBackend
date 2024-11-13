from django.db import models
from users.models import User
from vehicles.models import Vehicle



class PCN(models.Model):
    ticket_type = models.CharField(max_length =300)
    pcn = models.TextField()
    date_of_notice = models.DateField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    front_ticket_image = models.ImageField(upload_to="front_ticket_image/")
    back_ticket_image = models.ImageField(upload_to="back_ticket_image/")
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.date_of_notice
    
    class Meta:
        ordering =("-id",)
    