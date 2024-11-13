import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from utils.ResponseGenerator import ResponseGenerator
from users.serializers import SignUpSerializer
from rest_framework import status
from rest_framework.views import APIView

stripe.api_key = settings.STRIPE_SECRET_KEY



class UpgradeUserSubscriptionPlan(APIView):
    def put(self, request):
        subscription = request.data.get("subscription")
        user = request.user
        user.subscription = subscription
        user.save()
        
        return ResponseGenerator.response(
            data=SignUpSerializer(user).data,
            status=status.HTTP_200_OK,
            message="User subscription updated successfully"
        )



class CreateSubscriptionIntent(APIView):
    def post(self,request):
        amount = request.data.get('amount')
        user = request.user
        customer = stripe.Customer.retrieve(user.stripe_id)
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount *  100), 
                currency="gbp",  
                metadata={"integration_check": "subscription_payment"},  
                payment_method_types=["card"],  
                customer=customer
            )
            return ResponseGenerator.response(data=payment_intent, status=status.HTTP_201_CREATED, message="Intent created successfully")
        
        
        
        except stripe.error.StripeError as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)
       
