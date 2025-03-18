import json
import threading
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.timezone import now
from datetime import datetime, timedelta, timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import stripe
from firebase_admin import messaging
from django.template.loader import render_to_string
from subscriptions.models import Subscription
from subscriptions.views import handleReferalCreditting, userSubscriptionNotification
from users.models import DeviceToken, User, VerificationSession
from utils.tasks import send_email, verify_user_documents  

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET



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

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    print("stripe hook started")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    
    print(event.type)
    

    # Handle the event
    if event.type == 'customer.subscription.trial_will_end':
        handle_trial_will_end(event.data.object)
    if event.type == "customer.subscription.created":
        handle_subscription_created(event.data.object)
    elif event.type == 'customer.subscription.updated':
        handle_subscription_updated(event.data.object)
    elif event.type == 'invoice.payment_succeeded':
        handle_payment_succeeded(event.data.object)
    elif event.type == 'invoice.payment_failed':
        handle_payment_failed(event.data.object)
    
    elif event.type == 'identity.verification_session.verified':
        handle_verified_session(event.data.object)
    elif event.type == 'identity.verification_session.requires_input':
        print("Require input")
        handle_requires_input(event.data.object)
    elif event.type == 'identity.verification_session.canceled':
        handle_canceled_session(event.data.object)
    elif event['type'] == 'identity.verification_session.processing':
        session = event['data']['object']
        verification = VerificationSession.objects.get(
            stripe_session_id=session.id
        )
        user = User.objects.get(email = verification.user.email)
        
        try:
            user.document_verified = True
            user.save()
        except User.DoesNotExist:
            return HttpResponse(status=404)

    return HttpResponse(status=200)


def onsub(subscription):
    user = User.objects.get(id=subscription.metadata.get('user_id'))
    name = subscription.metadata.get('name')
    walletCount = subscription.metadata.get('walletCount')
    period = subscription.metadata.get('period')
    
    subscription = Subscription.objects.create(
        name=name,
        period=period,
    )
    user.subscription = subscription
    user.isSubbedBefore = True
    user.vehicle_count = 0
    user.pcn_count = 0
    user.walletCount = walletCount
    user.date_for_next_pcn_upload = now().date() + timedelta(days=13)
    user.save()
    
    t = threading.Thread(target=userSubscriptionNotification, args=(user,))
    t.start()
    
    handleReferalCreditting(instance=user)



def handle_verified_session(session):
    verification = VerificationSession.objects.get(
        stripe_session_id=session.id
    )
    user = User.objects.get(email = verification.user.email)
    if user.subscription and user.subscription.date_subscripted:
        subscribed_date_plus4_days = user.subscription.date_subscripted + timedelta(days=4)

        # Get today's date (using Django's timezone-aware now)
        today = timezone.now().date()
        
        if hasattr(subscribed_date_plus4_days, 'date'):
            subscribed_date_plus4_days = subscribed_date_plus4_days.date()
            
        
        days_difference = (today - subscribed_date_plus4_days ).days
        
        if days_difference < 0:
            target_date = timezone.now() + timedelta(days=days_difference)
    
            minute = target_date.minute
            hour = target_date.hour
            day = target_date.day
            month = target_date.month
            day_of_week = target_date.weekday()  
            
            crontab, _ = CrontabSchedule.objects.get_or_create(
                minute=minute,
                hour=hour,
                day_of_month=day,
                month_of_year=month,
                day_of_week=day_of_week,
            )
            

            PeriodicTask.objects.create(
                crontab=crontab,
                task="utils.tasks.verify_user_account_document",
                name=f"self.task_name_{user.id}_{verification.id}",
                args=json.dumps([user.id, verification.id]),
                one_off=True,
            )

        else:
            verify_user_documents(user_id=user.id, verification_id=verification.id)
            
            ## Verify user
            
    else:
        ## USER NOT SUBSCRIBED
        pass

def handle_requires_input(session):
    verification = VerificationSession.objects.get(
        stripe_session_id=session.id
    )
    
    verification.status = 'requires_input'
    verification.save()
    
    
    user = User.objects.get(email = verification.user.email)
    message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
       We are not able to verify your identity. Please try again.
        '''})
        
    t = threading.Thread(target=send_email, args=(f"Documents verification", message,[user.email]))
    t.start()
    
    
    send_mobile_notification(
            user,
            title="Documents verification",
            message="We are not able to verify your identity. Please try again."
            
        )
    
    

def handle_canceled_session(session):
    verification = VerificationSession.objects.get(
        stripe_session_id=session.id
    )
    verification.status = 'canceled'
    verification.save()
    
    user = User.objects.get(email = verification.user.email)
    message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
        We are not able to verify your identity. Please try again.
        '''})
        
    t = threading.Thread(target=send_email, args=(f"Documents verification", message,[user.email]))
    t.start()
    
    send_mobile_notification(
            user,
            title="Documents verification",
            message="We are not able to verify your identity. Please try again."
            
        )

def handle_subscription_created(subscription):
    try:
        onsub(subscription=subscription)

        
    except User.DoesNotExist as exception:
        print(exception)
        print(f"User not found for subscription: {subscription.id}")
        
        
def handle_trial_will_end(subscription):
    # Get user from subscription metadata
    try:
        user = User.objects.get(id=subscription.metadata.get('user_id'))
        message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
        Your trial will end in 3 days.
        '''})
        
        t = threading.Thread(target=send_email, args=(f"Subscription cancellation", message,[user.email]))
        t.start()
        
    except User.DoesNotExist:
        print(f"User not found for subscription: {subscription.id}")

def handle_subscription_updated(subscription):
    try:
        user = User.objects.get(id=subscription.metadata.get('user_id'))
        if subscription.status == 'active':
             onsub(subscription=subscription)
        elif subscription.status in ['incomplete', 'past_due']:
            user.subscription = None
            message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
            Your subscription has been cancelled. Please renew to continue using PCN.
            '''})
            
            t = threading.Thread(target=send_email, args=(f"Subscription cancelled", message,[user.email]))
            t.start()
        
        user.save()
    except User.DoesNotExist:
        print(f"User not found for subscription: {subscription.id}")

def handle_payment_succeeded(invoice):
    subscription = stripe.Subscription.retrieve(invoice.subscription)
    try:
        user = User.objects.get(id=subscription.metadata.get('user_id'))
        message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
        Your subscription payment was successfully
        '''})
        
        t = threading.Thread(target=send_email, args=(f"Subscription paid", message,[user.email]))
        t.start()
    except User.DoesNotExist:
        print(f"User not found for invoice: {invoice.id}")

def handle_payment_failed(invoice):
    subscription = stripe.Subscription.retrieve(invoice.subscription)
    try:
        user = User.objects.get(id=subscription.metadata.get('user_id'))
        user.subscription = None
        user.save()
        
        message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
        Your subscription payment was not successful. Please renew to continue using PCN.
        '''})
        
        t = threading.Thread(target=send_email, args=(f"Subscription cancelled", message,[user.email]))
        t.start()
        
       
    except User.DoesNotExist:
        print(f"User not found for invoice: {invoice.id}")
