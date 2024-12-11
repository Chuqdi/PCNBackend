from django.db import models



class ContactUsEmail(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return self.message
    
    
    
    
class SubscriptionEmail(models.Model):
    email = models.EmailField()
    date_subscribed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email