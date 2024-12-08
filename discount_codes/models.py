from enum import Enum
from django.db import models






class DurationEnum(Enum):
    ONCE = "once"
    # FOREVER = "forever"
    REPEATING ="repeating"
    
class DiscountCode(models.Model):
    code = models.CharField(max_length=255, unique=True)
    percentage_off = models.IntegerField()
    duration_in_months=models.IntegerField()
    duration = models.CharField(max_length=400, choices=[(status.name, status.value) for status in DurationEnum], default="forever")
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.code