
from django.db.models.signals import post_save
from users.models import DeviceToken
from .models import Notification
from django.dispatch import receiver
from firebase_admin import messaging







@receiver(post_save, sender=Notification) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        title = instance.title
        message = instance.message
        expired_data = instance.expired_data
        screen = instance.screen
        
        
        try:
            user_token = DeviceToken.objects.get(user = instance.user)
            n_message = messaging.Message(
            notification=messaging.Notification(
                title={
                    "title": title,
                    "message": message,
                    "expired_data":expired_data,
                    "screen":screen,
                    "is_notification": True
                    },
                body=message,
            ),
            token=user_token.token.strip(),
        )
            messaging.send(n_message)
            print("sent")
        except Exception as e:
            print(e)

