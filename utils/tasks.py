import threading
from celery import shared_task
from users.models import  DeviceToken, User
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from celery import shared_task
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from users.models import VerificationSession
from firebase_admin import messaging





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



def verify_user_documents(user_id, verification_id):
    if user.subscription and user.subscription.date_subscripted:
    
        verification = VerificationSession.objects.get(id=verification_id)
        user = User.objects.get(id = user_id)
        verification.status = 'verified'
        user.document_verified = True
        user.save()
        message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
            Documents verification
            '''})
        
            
        t = threading.Thread(target=send_email, args=(f"Documents verified", message,[user.email]))
        t.start()
        # verification.verification_details = session.verified_outputs
        
        
        
        send_mobile_notification(
                user,
                title="Documents verification",
                message="Documents verified"
                
            )

        verification.save()



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
    print(recipient_list)
    print("email sent")




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
            ,"btnTitle":"Get Your Cover Now", "btnLink":"https://www.pcnticket.com/#pricings"})
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
                ,"btnTitle":"Buy Cover Now", "btnLink":"https://www.pcnticket.com/#pricings"})
            
            
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
            ,"btnTitle":"Buy Cover Now", "btnLink":"https://www.pcnticket.com/#pricings"})
        
        
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
            ,"btnTitle":"Buy Cover Now", "btnLink":"https://www.pcnticket.com/#pricings"})
            
            
            try:
                send_email(
                    message=message,
                    recipient_list=[user.email],
                    subject=title,
                    
                )
            except Exception as e:
                print(f"Error sending email: {e}")





        



@shared_task
def verify_user_account_document(user_id, verification_id):
    verify_user_documents(user_id=user_id, verification_id=verification_id)