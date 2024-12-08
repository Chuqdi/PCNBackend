from django.shortcuts import render
from rest_framework.views import APIView
import stripe
from django.conf import settings
from django.http import JsonResponse
from discount_codes.models import DiscountCode
from django.views.decorators.csrf import csrf_exempt



stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def delete_all_promotion_codes(request):

    try:
        # List all promotion codes
        promotion_codes = stripe.PromotionCode.list(limit=100) 
        for promo_code in promotion_codes.auto_paging_iter():
            stripe.PromotionCode.delete(promo_code.id)
        
        return JsonResponse({"message": "All promotion codes deleted successfully."})

    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_all_coupons(request):
    """
    Delete all coupons from Stripe.
    """
    try:
        # List all coupons
        coupons = stripe.Coupon.list(limit=100)  # Adjust limit as needed

        # Delete each coupon
        for coupon in coupons.auto_paging_iter():
            stripe.Coupon.delete(coupon.id)
        
        return JsonResponse({"message": "All coupons deleted successfully."})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
    
    
    
class CreateDiscountCodeView(APIView): 
    def post(self, request):
        DiscountCode.objects.all().delete()
        code = request.data.get("code")
        instance = DiscountCode.objects.create(
            code=code,
            percentage_off=request.data.get("percentage_off"),
            duration=request.data.get("duration"),
            duration_in_months=request.data.get("duration_in_months")
        )
        try:
            stripe.PromotionCode.list().clear()
            coupon = stripe.Coupon.create(
            percent_off=instance.percentage_off,
            duration=instance.duration,
            duration_in_months = instance.duration_in_months
            )
            promo =stripe.PromotionCode.create(
            coupon=coupon.id,
            code=instance.code,  
            )
            print(promo)
            print("completd")
            
        except stripe.error.StripeError as e:
            print(e)
            return {"error": str(e)}

