
from django.db.models.signals import post_save
from .models import DiscountCode
from django.dispatch import receiver
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY





@receiver(post_save, sender=DiscountCode) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            coupon = stripe.Coupon.create(
            percent_off=instance.percentage_off,
            duration=instance.duration,
            duration_in_months = instance.duration_in_months
            )
            stripe.PromotionCode.create(
            coupon=coupon.id,
            code=instance.code,  
            )
            
        except stripe.error.StripeError as e:
            return {"error": str(e)}

