import threading
import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from subscriptions.models import Subscription
from utils.ResponseGenerator import ResponseGenerator
from users.serializers import SignUpSerializer
from rest_framework import status
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from users.models import DeviceToken, User
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
    For more information on ticket allowances please visit our <a href='https://www.usepcn.com/terms-and-conditions'>terms and conditions.</a>"""
    
    
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
    def put(self, request):
        name = request.data.get("name")
        walletCount = request.data.get("walletCount")
        period = request.data.get("period")
        is_one_off = request.data.get("isOneOff")
        
        subscription = Subscription.objects.create(
            name=name,
            period=period,
        )
        user = request.user
        user.subscription = subscription
        user.isSubbedBefore = True
        user.vehicle_count = 0
        user.pcn_count = 0
        user.walletCount = walletCount
        user.date_for_next_pcn_upload = now().date() + timedelta(days=13)
        user.save()
        
        
        scheduleNotificationFor2DaysBeforeCancelling(
            is_one_off=is_one_off,
            user=user,
            subscription=name
        )
        scheduleNotificationAfterCancelling(
            user=user,
            subscription=name
        )
        
        t = threading.Thread(target=userSubscriptionNotification, args=(user,))
        t.start()
        
        
        handleReferalCreditting(instance=user)
        
        
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
        customer = stripe.Customer.retrieve(user.stripe_id)
        try:
            if discountCode and len(discountCode) > 1:
                promotion_codes = stripe.PromotionCode.list(
                    code=discountCode  
                )
                if promotion_codes.data:
                    promotion_code = promotion_codes.data[0]
                    percent_off = promotion_code.coupon.percent_off
                    amount = amount - (percent_off/100 *amount)
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(amount *  100), 
                    currency="gbp",  
                    metadata={"integration_check": "subscription_payment"},  
                    payment_method_types=["card"],  
                    customer=customer,
                )
            else:
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(amount *  100), 
                    currency="gbp",  
                    metadata={"integration_check": "subscription_payment"},  
                    payment_method_types=["card"],  
                    customer=customer,
                )
                
            return ResponseGenerator.response(data={"payment_intent":payment_intent,"amount":amount}, status=status.HTTP_201_CREATED, message="Intent created successfully")
        
        
        
        except stripe.error.StripeError as e:
            print(e)
            return JsonResponse({
                "error": str(e)
            }, status=400)
       





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
        
        



        
        
        