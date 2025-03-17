
import threading
from django.db.models.signals import post_save
from firebase_admin import messaging
from users.models import DeviceToken
from .models import Admin
from utils.tasks import send_email
from django.template.loader import render_to_string
from django.dispatch import receiver




@receiver(post_save, sender=Admin) 
def create_profile(sender, instance, created, **kwargs):
              
    if created:
        message = render_to_string("emails/message.html", { "name":instance.name,"message":f"""You have been invited as an admin to PCN. Use the link below. <br />
        <a href='http://localhost:3000/auth/register?email={instance.email}'>Accept Invite</a> """})
        t = threading.Thread(target=send_email, args=(f"PCN Submitted", message,[instance.user.email]))
        t.start()


