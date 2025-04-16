
import threading
from django.db.models.signals import post_save
from firebase_admin import messaging
from user_notifications.models import Notification
from users.models import DeviceToken
from .models import UserMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from utils.tasks import send_email





@receiver(post_save, sender=UserMessage) 
def create_profile(sender, instance:UserMessage, created, **kwargs):
    if created:
        if instance.as_email:
            message = render_to_string("emails/message.html", { "name":instance.user.full_name,"message":instance.content})
            t = threading.Thread(target=send_email, args=(instance.title, message,[instance.user.email]))
            t.start()
            
        
        if instance.as_mobile_notification:
            print(instance.user.email)
            try:
                user_token = DeviceToken.objects.get(user = instance.user)
                print(user_token.token)


                n_message = messaging.Message(
                notification=messaging.Notification(
                    data={
                    "screen":"Notifications",
                },
                    title=instance.title,
                    body=instance.content,
                ),
                token=user_token.token.strip(),
                
            )
                messaging.send(n_message)
            except Exception as e:
                print(e)
        
        if instance.user:
            n= Notification.objects.create(
                title =instance.title,
                message = instance.content,
                screen ="Notifications",
                user = instance.user
            )
            

