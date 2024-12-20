from django.shortcuts import render
from rest_framework.views import APIView
import stripe
from django.conf import settings
from django.http import JsonResponse
from discount_codes.models import DiscountCode
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from utils.ResponseGenerator import ResponseGenerator



stripe.api_key = settings.STRIPE_SECRET_KEY




class GetDiscountCodePercentOff(APIView):
    def get(self, request, ):
        discountCode = request.GET.get('code')
        percent_off = 0
        if discountCode and len(discountCode) > 1:
            promotion_codes = stripe.PromotionCode.list(
                code=discountCode  
            )
            coupons = stripe.Coupon.list()
            print(coupons)
            if coupons.data:
                promotion_code = coupons.data[0]
                percent_off = promotion_code.percent_off
                print(percent_off)

        
        return ResponseGenerator.response(data=percent_off, status=status.HTTP_200_OK, message="Discount retrieved")
        



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
            
        except stripe.error.StripeError as e:
            print(e)
            return {"error": str(e)}

