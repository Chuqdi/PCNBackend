
import json
import threading
from django.db.models.signals import post_save
from firebase_admin import messaging
from utils.tasks import send_email
from django.dispatch import receiver
from datetime import timedelta
from django.template.loader import render_to_string
from .models import User, DeviceToken
from django_celery_beat.models import CrontabSchedule, ClockedSchedule,PeriodicTask
from datetime import datetime, timedelta


    
    
    

def schedule_notifications( instance:User):
    print("notification email started")
    
    periodic_emails = [
        # 0.0833333333
        {
            "template":"first_reminder.html",
            "time_in_hours":0.03333333332,
            "subject":"Your PCN Is Ready to Meet You 👋",
        },
            {
            "template":"stop_just_appealing.html",
            "time_in_hours":24,
            "subject":"Discover the complete PCN experience"
            
        },
        {
            "template":"more_traffic_fines.html",
            "time_in_hours":(24 * 3),
            "subject":"Discover the complete PCN experience"
            
        },
            {
            "template":"benefits.html",
            "time_in_hours":(24 * 7),
            "subject":"Discover the complete PCN experience"
            
        },
        {
            "template":"social_proof.html",
            "time_in_hours":(24 * 10),
            "subject":"Discover the complete PCN experience"
            
        },
            {
            "template":"exclusive.html",
            "time_in_hours":(24 * 15),
            "subject":"Discover the complete PCN experience"
            
        },
            {
            "template":"education_email.html",
            "time_in_hours":(24 * 20),
            "subject":"Discover the complete PCN experience"
            
        },
            {
            "template":"urgency_email.html",
            "time_in_hours":(24 * 25),
            "subject":"Discover the complete PCN experience"

        },
            {
            "template":"case_study_email.html",
            "time_in_hours":(24 * 30),
            "subject":"Discover the complete PCN experience"
            
        },
        {
            "template":"reminder_with_countdown.html",
            "time_in_hours":(24 * 35),
            "subject":"Discover the complete PCN experience"
        },
         {
            "template":"win_back_email.html",
            "time_in_hours":(24 * 40),
            "subject":"Discover the complete PCN experience"
        },
          {
            "template":"almost_covered.html",
            "time_in_hours":(24 * 45),
            "subject":"Discover the complete PCN experience"
        },
       
        {
            "template":"second_reminder.html",
            "time_in_hours":(24 * 50),
            "subject":"Discover the complete PCN experience"
        }
         
         
    ]
    
    for periodic_email in periodic_emails:
        task_hour = periodic_email.get("time_in_hours")
        target_datetime = datetime.now() + timedelta(hours=task_hour)
        
        clocked_schedule = ClockedSchedule.objects.create(
            clocked_time=target_datetime
        )
        
        task_name = f"{instance.id}_{instance.email}_{task_hour}"
        try:
            PeriodicTask.objects.get(name=task_name).delete()
        except PeriodicTask.DoesNotExist:
            pass
        task = PeriodicTask.objects.create(
            clocked=clocked_schedule,
            task= f'utils.tasks.send_notification_email',
            name=task_name,
            one_off=True,
            kwargs=json.dumps({
                "user":instance.id,
                "template":periodic_email.get("template"),
                "subject":periodic_email.get("subject"),
                "plan":periodic_email.get("plan", False)
            })
        )
        print(task)
    
    
    print("notification email ended")
    
            
        
        

        
        




@receiver(post_save, sender=User) 
def user_created(sender, instance, created, **kwargs):
    if created:
        schedule_notifications(instance=instance)
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
                
        
        
        

        
        



        