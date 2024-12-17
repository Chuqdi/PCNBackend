from django.db import models

from users.models import User




class VirualCard(models.Model):
    cardholder_id = models.TextField()
    card_id = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE )
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.card_id