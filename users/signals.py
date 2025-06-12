
import json
import random
import threading
from django.db.models.signals import post_save
from firebase_admin import messaging
from utils.tasks import send_email
from .models import DeviceToken, User, VerificationSession
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from datetime import timedelta
from django.template.loader import render_to_string


    

@receiver(post_save, sender=User) 
def user_created(sender, instance, created, **kwargs):
    if created:
        refered_by_code = instance.refered_by_code
        if refered_by_code and len(refered_by_code) > 1:
            referer = User.objects.filter(referalCode = refered_by_code)
            if referer.exists():
                referer= referer[0]
                referer.walletCount = referer.walletCount + 20
                referer.save()
                
                title = "Thanks for Your Referral"
                messageText = f"You have recieved 20 wallet credit following a referal sign up using your code by {instance.full_name}"
                
                message = render_to_string("emails/message.html", { "name":instance.full_name,"message":messageText})
                t = threading.Thread(target=send_email, args=(title, message,[referer.email]))
                t.start()
                
                
                try:
                    user_token = DeviceToken.objects.get(user = referer)


                    n_message = messaging.Message(
                        data={
                            "screen":"Home",
                        },
                    notification=messaging.Notification(
                        title=title,
                        body=messageText,
                    ),
                    token=user_token.token.strip(),
                )
                    messaging.send(n_message)
                    print("sent mobile")
                except Exception as e:
                    print(e)
                
        
        
        

        
        



        