
import threading
from django.db.models.signals import post_save
from .models import ContactUsEmail
from utils.tasks import send_email
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.conf import settings




@receiver(post_save, sender=ContactUsEmail) 
def create_profile(sender, instance, created, **kwargs):
    if  created:
        message = render_to_string("emails/message.html", { "name":"Admin",
        "message":f"""
        First name:{instance.first_name}
        Last name:{instance.last_name}
        Email:{instance.email}
        Message<br />
        {instance.message}
        """})
        t = threading.Thread(target=send_email, args=(f"Contact Message", message,[settings.EMAIL_HOST_USER,"usepcn.com@gmail.com"]))
        t.start()
        