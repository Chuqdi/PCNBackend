
import threading
from django.db.models.signals import post_save
from .models import PCN
from users.models import DeviceToken, User
from firebase_admin import messaging
from utils.tasks import send_email
from django.template.loader import render_to_string
from django.dispatch import receiver




def send_mobile_notification(user:User, title:str,message:str,):
    try:
        user_token = DeviceToken.objects.get(user = user)
        n_message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message,
        ),
        data={},
        token=user_token.token.strip(),
    )
        messaging.send(n_message)
    except Exception as e:
        print(e)

@receiver(post_save, sender=PCN) 
def create_profile(sender, instance, created, **kwargs):
    if not created and  instance.is_denied:
        message = render_to_string("emails/ticket_denied.html", { "name":instance.user.full_name,"ticket":instance})
        t = threading.Thread(target=send_email, args=(f"Your PCN status update", message,[instance.user.email]))
        t.start()
        send_mobile_notification(instance.user, "Your PCN status update", "Your ticket was declined.")
    if not created and instance.is_paid:
        message = render_to_string("emails/ticket_approved.html", { "name":instance.user.full_name,"ticket":instance})
        t = threading.Thread(target=send_email, args=(f"Your PCN status update", message,[instance.user.email]))
        t.start()
        send_mobile_notification(instance.user, "Your PCN status update", "Your ticket has been settled.")
        
        
        
              
    if created:
        message = render_to_string("emails/ticket_created.html", { "name":instance.user.full_name,"ticket":instance})
        t = threading.Thread(target=send_email, args=(f"PCN Submitted", message,[instance.user.email]))
        t.start()
        send_mobile_notification(instance.user, "Your PCN status update", "Your ticket has been submitted.")
        



#         try:
#             user_token = DeviceToken.objects.get(user = instance.user)


#             n_message = messaging.Message(
#             notification=messaging.Notification(
#                 title="We are processing your ticket payment",
#                 body="We have received your PCN payment request and are currently processing it. Please find the details below.",
#             ),
#             token=user_token.token.strip(),
#         )
#             messaging.send(n_message)
#             print("sent")
#         except Exception as e:
#             print(e)