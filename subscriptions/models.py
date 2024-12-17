from django.db import models
from enum import Enum
from django.utils import timezone

class SubscriptionPeriodType(Enum):
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"

class SubscriptionType(Enum):
    BASIC = "BASIC"
    PREMIUM = "PREMIUM"
    
    
class Subscription(models.Model):
    name = models.CharField(max_length=200, 
      choices=[(status.name, status.value) for status in SubscriptionType],  
      null=True, blank=True)
    period = models.CharField(max_length=200, 
      choices=[(status.name, status.value) for status in SubscriptionPeriodType],  
      null=True, blank=True)
    is_one_off = models.BooleanField(default=False)
    date_subscripted = models.DateTimeField(default=timezone.now)
    
    
  
  

    