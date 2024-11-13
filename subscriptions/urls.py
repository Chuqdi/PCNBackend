from django.urls import path
from .views import CreateSubscriptionIntent, UpgradeUserSubscriptionPlan


urlpatterns = [
    path("create_intent/",CreateSubscriptionIntent.as_view(), ),
    path("update_user_subscription/",UpgradeUserSubscriptionPlan.as_view(), ),
    
]
