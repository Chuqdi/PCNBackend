
import threading
from django.db.models.signals import post_save
from firebase_admin import messaging
from users.models import DeviceToken
from .models import Chat
from utils.tasks import send_email
from django.template.loader import render_to_string
from django.dispatch import receiver




@receiver(post_save, sender=Chat) 
def create_profile(sender, instance, created, **kwargs):
    if  created and not instance.sent:
        message = render_to_string("emails/message.html", { "name":instance.user.full_name,"message":instance.message})
        t = threading.Thread(target=send_email, args=(f"Support team", message,[instance.user.email]))
        t.start()
        print("singla running")
        
        
        try:
            user_token = DeviceToken.objects.get(user = instance.user)


            n_message = messaging.Message(
                data={
                    "screen":"Profile",
                    "show_support_messages":"1"
                },
            notification=messaging.Notification(
                title="Support Team",
                body=instance.message,
            ),
            token=user_token.token.strip(),
        )
            messaging.send(n_message)
        except Exception as e:
            print(e)