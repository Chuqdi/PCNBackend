import threading
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.timezone import now
from datetime import datetime, timedelta
import stripe
from django.template.loader import render_to_string
from subscriptions.models import Subscription
from subscriptions.views import handleReferalCreditting, userSubscriptionNotification
from users.models import User, VerificationSession
from utils.tasks import send_email  

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

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
        handle_requires_input(event.data.object)
    elif event.type == 'identity.verification_session.canceled':
        handle_canceled_session(event.data.object)

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
    verification.status = 'verified'
    user = User.objects.get(email = verification.user.email)
    user.document_verified = True
    user.save()
    message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
        Documents verified successfully
        '''})
    
    print("verification")
    print(verification)
        
    t = threading.Thread(target=send_email, args=(f"Documents verified", message,[user.email]))
    t.start()
    # verification.verification_details = session.verified_outputs
    verification.save()

def handle_requires_input(session):
    verification = VerificationSession.objects.get(
        stripe_session_id=session.id
    )
    
    verification.status = 'requires_input'
    verification.save()
    print("verification")
    print(verification)
    
    
    user = User.objects.get(email = verification.user.email)
    message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
        Documents verified failed. More input required
        '''})
        
    t = threading.Thread(target=send_email, args=(f"Documents verified", message,[user.email]))
    t.start()
    
    

def handle_canceled_session(session):
    verification = VerificationSession.objects.get(
        stripe_session_id=session.id
    )
    verification.status = 'canceled'
    verification.save()
    print("verification")
    print(verification)
    
    user = User.objects.get(email = verification.user.email)
    message = render_to_string("emails/message.html", { "name":user.full_name,"message":'''
        Documents verified was cancelled
        '''})
        
    t = threading.Thread(target=send_email, args=(f"Documents verified", message,[user.email]))
    t.start()

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
