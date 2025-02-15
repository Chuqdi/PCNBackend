import threading
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from subscriptions.models import Subscription
from utils.ResponseGenerator import ResponseGenerator
from users.serializers import SignUpSerializer
from rest_framework import status
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from rest_framework import permissions
from users.models import DeviceToken, User,VerificationSession
import json
from datetime import timedelta
from django.utils.timezone import now
from django.template.loader import render_to_string
from utils.tasks import  send_email
from firebase_admin import messaging
stripe.api_key = settings.STRIPE_SECRET_KEY



def handleReferalCreditting(instance:User):
        if not instance.isReferalUsed and instance.refered_by_code:
            referalTitle="Referal bonus"
            referalMessage = "You have received a £5 referal bonus"
            refered_by = User.objects.get(referalCode = instance.refered_by_code)
            refered = instance
            
            refered_by.walletCount = refered_by.walletCount + settings.REFERAL_CREDIT_AMOUNT
            refered_by.save()
            refered.walletCount = refered.walletCount + settings.REFERAL_CREDIT_AMOUNT
            refered.isReferalUsed = True
            refered.save()
            
            
            
            
            message = render_to_string("emails/message.html", { "name":refered_by.full_name,"message":referalMessage})
            t = threading.Thread(target=send_email, args=(referalTitle, message,[refered_by.email]))
            t.start()
            
            message = render_to_string("emails/message.html", { "name":refered.full_name,"message":referalMessage})
            t = threading.Thread(target=send_email, args=(referalTitle, message,[refered.email]))
            t.start()



            try:
                user_token = DeviceToken.objects.get(user = refered_by)


                n_message = messaging.Message(
                notification=messaging.Notification(
                    title=referalTitle,
                    body=referalMessage,
                ),
                token=user_token.token.strip(),
            )
                messaging.send(n_message)
                print("sent")
            except Exception as e:
                print(e)
                
            try:
                user_token = DeviceToken.objects.get(user = refered)


                n_message = messaging.Message(
                notification=messaging.Notification(
                    title=referalTitle,
                    body=referalMessage,
                ),
                token=user_token.token.strip(),
            )
                messaging.send(n_message)
                print("sent")
            except Exception as e:
                print(e)

def userSubscriptionNotification(user:User):
    title="Your cover purchase was successful"
    body=f"""Your {user.subscription.name} purchase was successful. <br /><br />
    You are covered and you can upload your first ticket 13 days from now. <br /><br />
    For more information on ticket allowances please visit our <a href='https://www.pcnticket.com/terms-and-conditions'>terms and conditions.</a>"""
    
    
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
            body="You are covered and you can upload your first ticket 13 days from now.",
        ),
        token=user_token.token.strip(),
    )
        messaging.send(n_message)
        print("sent")
    except Exception as e:
        print(e)


def scheduleNotificationAfterCancelling(user:User, subscription:str):
        today = datetime.today()
        if subscription == "BASIC":
            next_month = today + relativedelta(month=4)
        else:
            next_month = today + relativedelta(year=1)
        
        crontab,created = CrontabSchedule.objects.get_or_create(
            minute=next_month.minute,
            hour=next_month.hour,
            day_of_month=next_month.day,
            month_of_year=next_month.month
        )
        task_name = f"user_subscription_notification_after_cancelling_{user.id}"
        try:
            PeriodicTask.objects.get(name=task_name).delete()
        except PeriodicTask.DoesNotExist:
            pass
        PeriodicTask.objects.create(
            crontab=crontab,
            task='utils.tasks.user_subscription_notification_after_cancelling',
            name=task_name,
            args=json.dumps(user.pk)
        )
        

    
def scheduleNotificationFor2DaysBeforeCancelling(is_one_off:bool,user:User, subscription:str):
    if not is_one_off:
        today = datetime.today()
        next_month = today + relativedelta(months=1)
        target_date = next_month - timedelta(days=2)
        
        crontab,created = CrontabSchedule.objects.get_or_create(
            minute=target_date.minute,
            hour=target_date.hour,
            day_of_month=target_date.day,
            month_of_year=target_date.month
        )
        task_name = f"user_subscription_notification_two_days_before_cancelling_{user.id}"
        try:
            PeriodicTask.objects.get(name=task_name).delete()
        except PeriodicTask.DoesNotExist:
            pass
        PeriodicTask.objects.create(
            crontab=crontab,
            task='utils.tasks.user_subscription_notification_two_days_before_cancelling',
            name=task_name,
            args=json.dumps(user.pk)
        )
    else:
        today = datetime.today()
        if subscription == "BASIC":
            next_month = today + relativedelta(month=4)
        else:
            next_month = today + relativedelta(year=1)
        target_date = next_month - timedelta(days=2)
        
        crontab,created = CrontabSchedule.objects.get_or_create(
            minute=target_date.minute,
            hour=target_date.hour,
            day_of_month=target_date.day,
            month_of_year=target_date.month
        )
        task_name = f"user_subscription_notification_two_days_before_cancelling_{user.id}"
        try:
            PeriodicTask.objects.get(name=task_name).delete()
        except PeriodicTask.DoesNotExist:
            pass
        PeriodicTask.objects.create(
            crontab=crontab,
            task='utils.tasks.user_subscription_notification_two_days_before_cancelling',
            name=task_name,
            args=json.dumps(user.pk)
        )
        


class UpgradeUserSubscriptionPlan(APIView):
    permission_classes = [permissions.AllowAny]
    def put(self, request):
        name = request.data.get("name")
        walletCount = request.data.get("walletCount")
        period = request.data.get("period")
        is_one_off = request.data.get("isOneOff")
        email = request.data.get("email")
        
        subscription = Subscription.objects.create(
            name=name,
            period=period,
        )
        user = User.objects.get(email=email)
        user.subscription = subscription
        user.isSubbedBefore = True
        user.vehicle_count = 0
        user.pcn_count = 0
        user.walletCount = walletCount
        user.date_for_next_pcn_upload = now().date() + timedelta(days=13)
        
        
        # user.save()
        
        
        # scheduleNotificationFor2DaysBeforeCancelling(
        #     is_one_off=is_one_off,
        #     user=user,
        #     subscription=name
        # )
        # scheduleNotificationAfterCancelling(
        #     user=user,
        #     subscription=name
        # )
        
        # t = threading.Thread(target=userSubscriptionNotification, args=(user,))
        # t.start()
        
        
        # handleReferalCreditting(instance=user)
        
        
        return ResponseGenerator.response(
            data=SignUpSerializer(user).data,
            status=status.HTTP_200_OK,
            message="User subscription updated successfully"
        )

class CreateSubscriptionIntent(APIView):
    def post(self,request):
        amount = request.data.get('amount')
        user = request.user
        discountCode = request.data.get("discountCode")
        priceId = request.data.get('priceId')
        name = request.data.get('name')
        walletCount = request.data.get('walletCount')
        peroid = request.data.get('peroid')
        joiningFee = request.data.get('joiningFee')
        isOneOff= request.data.get("isOneOff")
        isMobile= request.data.get("isMobile","0")
        isLastCover = request.data.get("isLastCover", 0)
        
        
        
        
        
        # price_1QXftWEaYyTuzzYVRuJV7WdV
        line_items =[
                {
                   "price":priceId,
                    "quantity":1
        }]
        subscription_data ={
            'metadata': {
                    'user_id': str(user.id), 
                    "walletCount" : walletCount,
                    'user_id': str(user.id),  
                    "name" : name,
                    "walletCount" : walletCount,
                    "period" : peroid,
                    "is_one_off" : isOneOff,
                    "email":user.email
            }
        }
        
       
        if isLastCover==1 and  not user.isSubbedBefore:
            line_items.append({
                "price":joiningFee,
                'quantity': 1,
            })
        if isLastCover==0:
            subscription_data["trial_period_days"] =14
            

        success_url = f'https://www.pcnticket.com/?paymentModal=1&walletCount={walletCount}&name={name}&is_one_off={isOneOff}&peroid={peroid}&email={user.email}&isMobile={isMobile}'
        cancel_url = f'https://www.pcnticket.com/?payment_cancelled=1&isMobile={isMobile}'
        
        if discountCode and len(discountCode) > 1:
            session = stripe.Subscription.create(
                payment_method_types=['card'],
                items=line_items,
                mode='subscription',
                trial_period_days=14,
                customer=user.stripe_id,
                success_url=success_url,
                cancel_url=cancel_url,
                subscription_data=subscription_data,
                discounts=[{
                    "coupon":discountCode,
                }]
            )
        else:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='subscription',
                customer=user.stripe_id,
                success_url=success_url,
                cancel_url=cancel_url,
                subscription_data=subscription_data,
            )
        
        return ResponseGenerator.response(data={"payment_intent":session.get("id"),"url":session.get("url"),"amount":amount}, status=status.HTTP_201_CREATED, message="Intent created successfully")
        
        
        
    





class CancelSubscription(APIView):
    def put(self, request):
        user = request.user
        user.subscription =None
        user.walletCount = 0
        user.save()
        
        
        message = render_to_string("emails/message.html", { "name":user.full_name,"message":"Subscription cancelled successfully"})
        t = threading.Thread(target=send_email, args=(f"Subscription cancelled", message,[user.email]))
        t.start()
        
        
        return ResponseGenerator.response(
            data=SignUpSerializer(user).data,
            status=status.HTTP_200_OK,
            message="User subscription cancelled successfully"
        )
        
        



        
        
        
        
        
class VerificationViews(APIView):
    def post(self, request):
        try:
            verification_session = stripe.identity.VerificationSession.create(
                type='document',
                metadata={
                    'user_id': str(request.user.id),
                },
                options={
                    'document': {
                        'allowed_types': ['driving_license', 'passport', 'id_card'],
                        'require_id_number': True,
                        'require_live_capture': True,
                        'require_matching_selfie': True,
                    }
                },
                return_url="https://www.pcnticket.com",
            )

            VerificationSession.objects.create(
                user=request.user,
                stripe_session_id=verification_session.id,
                status='pending'
            )
            
            return ResponseGenerator.response(
                data=verification_session.client_secret,
                status=status.HTTP_200_OK,
                message="Verification session created successfully"
            )

            
        except Exception as e:
            return ResponseGenerator.response(
                data={},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred while creating verification session"
            )
