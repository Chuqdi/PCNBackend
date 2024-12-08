from django.urls import path
from .views import CreateSubscriptionIntent, UpgradeUserSubscriptionPlan, CancelSubscription


urlpatterns = [
    path("create_intent/",CreateSubscriptionIntent.as_view(), ),
    
    path("update_user_subscription/",UpgradeUserSubscriptionPlan.as_view(), ),
    path("cancel/", CancelSubscription.as_view(), ),
    
]
