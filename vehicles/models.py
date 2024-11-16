from django.db import models
from users.models import User
from django.utils import timezone

class Vehicle(models.Model):
    vehicle_number = models.TextField()
    vehicle_make = models.TextField()
    color = models.TextField(null=True, blank=True)
    vehicle_image = models.ImageField(upload_to="vehicle_images/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_date_editted = models.DateTimeField(auto_now=True)
    
    def __str__(self, request):
        return self.vehicle_number
    
    
    class Meta:
        ordering =("-id",)
    
    