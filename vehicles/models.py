from django.db import models
from users.models import User

class Vehicle(models.Model):
    vehicle_number = models.TextField()
    vehicle_make = models.TextField()
    color = models.TextField()
    vehicle_image = models.ImageField(upload_to="vehicle_images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self, request):
        return self.vehicle_number
    
    
    class Meta:
        ordering =("-id",)
    
    