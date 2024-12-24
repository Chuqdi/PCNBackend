from celery import shared_task
from users.models import  User
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from celery import shared_task
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta





@shared_task
def test_async(bind=True):
    message = EmailMessage("subject", "message",  settings.DEFAULT_FROM_EMAIL,["morganhezekiah111@gmail.com"])
    message.content_subtype = 'html' 
    message.send()



@shared_task
def send_email( subject, message, recipient_list, ):
    message = EmailMessage(subject, message,  settings.DEFAULT_FROM_EMAIL,recipient_list)
    message.content_subtype = 'html' 
    message.send()




@shared_task
def send_user_first_subscription_message():
    now = timezone.now()

    one_day_ago = now - timedelta(days=1)

    users = User.objects.filter(date_joined__date=one_day_ago.date())
        
    for user in users:
        if not user.subscription:
            title ="Notification"
            
            message = render_to_string("emails/message.html", {"name":user.full_name,
                                                        "message":"""
                                                        Thanks for downloading <b>PCN Ticket</b>! Managing parking tickets just got easier. Did you know you can cover your fines directly through the app? With a PCN Cover, we handle the hassle for you: pay your fine or even contest unfair tickets!
                                                        """
                ,"btnTitle":"Get Your Cover Now", "btnLink":"https://www.usepcn.com/#pricings"})
            
            
            try:
                send_email(
                    message=message,
                    recipient_list=[user.email],
                    subject=title,
                    
                )
            except Exception as e:
                print(f"Error sending email: {e}")




@shared_task
def send_user_second_subscription_message():
    now = timezone.now()

    one_day_ago = now - timedelta(days=1)

    users = User.objects.filter(date_joined__date=one_day_ago.date())
    for user in users:
        if not user.subscription:
            title ="Notification"
            
            message = render_to_string("emails/message.html", {"name":user.full_name,
                                                        "message":"""
                                                        Did you know the average parking fine doubles if left unpaid? Stay ahead with a PCN Cover. We’ll handle your fines quickly and help avoid late fees.
                                                        <br />
                                                        <p>🔒 <b>Secure your peace of mind today:</b></p>
                                                        """
                ,"btnTitle":"Buy Cover Now", "btnLink":"https://www.usepcn.com/#pricings"})
            
            
            try:
                send_email(
                    message=message,
                    recipient_list=[user.email],
                    subject=title,
                    
                )
            except Exception as e:
                print(f"Error sending email: {e}")




@shared_task
def send_user_24_hr_subscription_message(user_id):
    user = User.objects.get(user_id=user_id)
    
    if not user.subscription:
        title ="Notification"
        
        message = render_to_string("emails/message.html", {"name":user.full_name,
                                                    "message":"""
                                                    Did you know the average parking fine doubles if left unpaid? Stay ahead with a PCN Cover. We’ll handle your fines quickly and help avoid late fees.
                                                    <br />
                                                    <p>🔒 <b>Secure your peace of mind today:</b></p>
                                                    """
            ,"btnTitle":"Buy Cover Now", "btnLink":"https://www.usepcn.com/#pricings"})
        
        
        try:
            send_email(
                message=message,
                recipient_list=[user.email],
                subject=title,
                
            )
        except Exception as e:
            print(f"Error sending email: {e}")




@shared_task
def send_user_fridays_subscription_message(user_id):
    users = User.objects.all()
    for user in users:
        if not user.subscription:
            title ="Notification"
            
            message = render_to_string("emails/message.html", {"name":user.full_name,
                                                        "message":"""
                                                        Did you know the average parking fine doubles if left unpaid? Stay ahead with a PCN Cover. We’ll handle your fines quickly and help avoid late fees.
                                                        <br />
                                                        <p>🔒 <b>Secure your peace of mind today:</b></p>
                                                        """
                ,"btnTitle":"Buy Cover Now", "btnLink":"https://www.usepcn.com/#pricings"})
            
            
            try:
                send_email(
                    message=message,
                    recipient_list=[user.email],
                    subject=title,
                    
                )
            except Exception as e:
                print(f"Error sending email: {e}")





        


