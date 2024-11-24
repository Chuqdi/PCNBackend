
import threading
from django.db.models.signals import post_save
from firebase_admin import messaging
from users.models import DeviceToken
from .models import PCN
from utils.tasks import send_email
from django.template.loader import render_to_string
from django.dispatch import receiver




@receiver(post_save, sender=PCN) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        message = render_to_string("emails/ticket_created.html", { "name":instance.user.full_name,"ticket":instance})
        t = threading.Thread(target=send_email, args=(f"Ticket Created", message,[instance.user.email]))
        t.start()



        try:
            user_token = DeviceToken.objects.get(user = instance.user)


            n_message = messaging.Message(
            notification=messaging.Notification(
                title="We are processing your ticket payment",
                body="We have received your ticket request and are currently processing it. Please find the details below",
            ),
            token=user_token.token.strip(),
        )
            messaging.send(n_message)
            print("sent")
        except Exception as e:
            print(e)