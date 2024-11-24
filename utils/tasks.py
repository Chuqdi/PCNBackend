import threading
from celery import shared_task
from utils.helpers import generateSecureEmailCredentials
from firebase_admin import messaging
from .EmailSender import SendEmail, send_activation_email
from users.models import DeviceToken, User
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage







JOB_APPLICATION_UPDATE ="Your job application update."


BOT_ACCOUNT_EMAILS = [
   "apextalents@yahoo.com",
   "leonstark@yahoo.com",
   "greenleaf@yahoo.com",
   "berkleyduffy@yahoo.com",
   "nexusstaffs@yahoo.com"
]



@shared_task
def user_subscription_notification_two_days_before_cancelling(user_id):
    user = User.objects.get(user_id=user_id)
    body ="Your subscription wil be cancelled in two days"
    title="Subscription cancelled"
    
    message = render_to_string("emails/message.html", { "name":user.full_name,"message":body})
    
    try:
        send_email(
            message=message,
            recipient_list=[user.email],
            subject=title,
            
        )
    except Exception as e:
        print(f"Error sending email: {e}")
    
    
    try:
        user_token = DeviceToken.objects.get(user = user)


        n_message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=user_token.token.strip(),
    )
        messaging.send(n_message)
        print("sent")
    except Exception as e:
        print(e)

@shared_task
def user_subscription_notification_after_cancelling(user_id):
    user = User.objects.get(user_id=user_id)
    user.subscription = None
    user.save()
    title="Subscription cancelled"
    body="Your subscription has been cancelled"
    
    
    message = render_to_string("emails/message.html", { "name":user.full_name,"message":body})
    try:
        send_email(
            message=message,
            recipient_list=[user.email],
            subject=title,
            
        )
    except Exception as e:
        print(f"Error sending email: {e}")
        
    try:
        user_token = DeviceToken.objects.get(user = user)


        n_message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=user_token.token.strip(),
    )
        messaging.send(n_message)
        print("sent")
    except Exception as e:
        print(e)



def botMessages(first_name:str, last_name:str, number):
    name = f"{first_name} {last_name}"
    message =""
    if number == 0:
        message= f"""Your resume stood out. We'd like to schedule an interview with you next week.
        Please reply immediately if you are interested as we have other candidates on our list.
        """
    elif number == 1:
        message= f"""We'd like to schedule an interview with you next week. Please let us know your availability.
        """
    elif number == 2:
        message= f"""Your application impressed us. When could you come in for an interview anytime soon?
        """
    elif number == 3:
        message= f"""We look forward to discussing how your skills align with our team’s goals. When are you available for an interview?
        """
    else:
        message= f"""Your background is impressive. We are eager to discuss how your skills can benefit our team during your interview.
        When are you free?
        """
    return message



@shared_task
def test():
    print("Yes on the task")









@shared_task
def sendUserActivationEmail(email, domain):
    user = User.objects.get(email=email)
    secureEmailCredentials = generateSecureEmailCredentials(user)
    token = secureEmailCredentials.get("token")
    uidb64 = secureEmailCredentials.get("uidb64")
    
    urlPath = f"{domain}/api/v1/users/activate_account/{token}/{uidb64}/"
    send_activation_email(
        user=user,
        template="emails/user_account_activation.html",
        urlPath=urlPath,
        subject="Account Email Activation",
    )



@shared_task
def actionNotificationEmail(message, to, title=""):
    template = render_to_string(
        "emails/action_notification.html", {"message": message, "title": title}
    )

    s = SendEmail(template=template, subject="Action Notification", to=(to,))









@shared_task
def send_email( subject, message, recipient_list, ):
    
    message = EmailMessage(subject, message,  settings.DEFAULT_FROM_EMAIL,recipient_list)
    message.content_subtype = 'html' 
    message.send()
    



@shared_task
def update_db_monthly_distributions():
    users = User.objects.all()
    for user in users:
        if user.is_active:
            user.number_of_distrubution_this_month =0
            user.number_of_notifications_this_month = 0
            user.number_of_notifications_this_month = 0
            user.save()








def sendNotificationEmail(name, message, to):
    message = render_to_string("emails/message.html", { "name":name, "message":message})
    t = threading.Thread(target=send_email, args=("Account Notification", message,[to,]))
    t.start()




# @shared_task
# def sendUserRoleNotifications8Hours():
#     roles = Role.objects.all()

#     for r in roles.iterator():
#         user = User.objects.get(email=r.user.email)
#         d = Distrubution.objects.filter(user= user)
#         if d.count() > 0 :
#             if user.subscription.upper() == settings.SUBSCRIPTIONTYPES[0].upper():
#                 if user.number_of_notifications_this_month < 5:
#                     user.number_of_notifications_this_month = user.number_of_notifications_this_month + 1
#                     user.save()
#                     title =JOB_APPLICATION_UPDATE
#                     message ="An employer just viewed your CV📝"
#                     sendNotificationEmail(name=f"{user.first_name} {user.last_name}", message=message, to=user.email)
#                     r.view_count = int(r.view_count) + 1
#                     r.save()
                


#                     try:
#                         user_token = DeviceToken.objects.get(user = user)

#                         n_message = messaging.Message(
#                         notification=messaging.Notification(
#                             title=title,
#                             body=message,
#                         ),
#                         token=user_token.token.strip(),
#                     )
#                         messaging.send(n_message)
#                     except:
#                         pass
                




# @shared_task
# def sendUserRoleNotifications10Hours():
#     roles = Role.objects.all()


#     for r in roles.iterator():
#         user = User.objects.get(email=r.user.email)
#         d = Distrubution.objects.filter(user= user)
#         if d.count() > 0 :
#             if  user.subscription.upper() != settings.SUBSCRIPTIONTYPES[0].upper():
#                 title =JOB_APPLICATION_UPDATE
#                 message ="Multiple employers has viewed your CV📝"
#                 r.view_count = int(r.view_count) + 1
#                 r.save()
#                 sendNotificationEmail(name=f"{user.first_name} {user.last_name}", message=message, to=user.email)

#                 try:
#                     user_token = DeviceToken.objects.get(user = user)

#                     n_message = messaging.Message(
#                     notification=messaging.Notification(
#                         title=title,
#                         body=message,
#                     ),
#                     token=user_token.token.strip(),
#                 )
#                     messaging.send(n_message)
#                 except:
#                     pass
                





@shared_task
def sendABotMessageToUser(reciept_id):
    message =f""
    sender = User.objects.get(email="morganhezekiah123@gmail.com")
    reciept = User.objects.get(id = reciept_id)
    UserMessage.objects.create(message=message, reciept=reciept, sender=sender)

# @shared_task
# def sendUserSubscriptionrRequestNotification():
  
#     users = User.objects.all()
#     for user in users.iterator():
#         messages = [
#             "Your CV is gaining traffic. Upgrade your plan to improve your chances of distributing your CV to more employers and getting hired faster.",
#             ""
#         ]
#         distributions = Distrubution.objects.filter(user = user)
#         if distributions.count() > 0:
#             if user.subscription.upper() != settings.SUBSCRIPTIONTYPES[4].upper():
#                 title = JOB_APPLICATION_UPDATE
#                 message = "Your CV is gaining traffic🔥. Upgrade your plan to improve your chances of distributing your CV to more employers and getting hired faster."
#                 sendNotificationEmail(name=f"{user.first_name} {user.last_name}", message=message, to=user.email)

#                 try:
#                     user_token = DeviceToken.objects.get(user = user)

#                     n_message = messaging.Message(
#                     notification=messaging.Notification(
#                         title=title,
#                         body=message,
#                     ),
#                     token=user_token.token.strip(),
#                 )
#                     messaging.send(n_message)
#                 except:
#                     pass


