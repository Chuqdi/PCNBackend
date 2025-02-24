from django.urls import path
from .views import CreateSubscriptionIntent, UpgradeUserSubscriptionPlan, CancelSubscription,VerificationViews, MobileDocumentVerification
from .stripe_webhook import stripe_webhook


urlpatterns = [
    path("create_intent/",CreateSubscriptionIntent.as_view(), ),
    path("update_user_subscription/",UpgradeUserSubscriptionPlan.as_view(), ),
    path("cancel/", CancelSubscription.as_view(), ),
    path("create_document_verification_session/<email>/", VerificationViews.as_view()),
    path("verification_sessions_mobile/", MobileDocumentVerification.as_view(),),
    path("stripe_webhooks/", stripe_webhook, ),
]
