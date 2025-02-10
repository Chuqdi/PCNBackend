import threading
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import stripe
from users.models import User
from utils.tasks import send_email  

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'customer.subscription.trial_will_end':
        handle_trial_will_end(event.data.object)
    elif event.type == 'customer.subscription.updated':
        handle_subscription_updated(event.data.object)
    elif event.type == 'invoice.payment_succeeded':
        handle_payment_succeeded(event.data.object)
    elif event.type == 'invoice.payment_failed':
        handle_payment_failed(event.data.object)

    return HttpResponse(status=200)

def handle_trial_will_end(subscription):
    # Get user from subscription metadata
    try:
        user = User.objects.get(id=subscription.metadata.get('user_id'))
        message ='''
        Your trial will end in 3 days.
        '''
        
        t = threading.Thread(target=send_email, args=(f"Subscription cancelled", message,[user.email]))
        t.start()
        
    except User.DoesNotExist:
        print(f"User not found for subscription: {subscription.id}")

def handle_subscription_updated(subscription):
    try:
        user = User.objects.get(id=subscription.metadata.get('user_id'))
        
        if subscription.trial_end:
            has_trial_ended = subscription.trial_end < stripe.Util.now()
            
            if has_trial_ended:
                if subscription.status == 'active':
                    message ='''
                    Your subscription has been renewed. Please renew to continue using PCN.
                    '''
                    t = threading.Thread(target=send_email, args=(f"Subscription cancelled", message,[user.email]))
                    t.start()
                elif subscription.status in ['incomplete', 'past_due']:
                    user.subscription = None
                    message ='''
                    Your subscription has been cancelled. Please renew to continue using PCN.
                    '''
                    
                    t = threading.Thread(target=send_email, args=(f"Subscription cancelled", message,[user.email]))
                    t.start()
                
                user.save()
    except User.DoesNotExist:
        print(f"User not found for subscription: {subscription.id}")

def handle_payment_succeeded(invoice):
    subscription = stripe.Subscription.retrieve(invoice.subscription)
    try:
        user = User.objects.get(id=subscription.metadata.get('user_id'))
        message ='''
        Your subscription payment was successfully
        '''
        
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
        message ='''
        Your subscription has been cancelled. Please renew to continue using PCN.
        '''
        
        t = threading.Thread(target=send_email, args=(f"Subscription cancelled", message,[user.email]))
        t.start()
    except User.DoesNotExist:
        print(f"User not found for invoice: {invoice.id}")
