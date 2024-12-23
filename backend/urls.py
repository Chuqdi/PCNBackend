
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.template.loader import render_to_string
from users.models import DeviceToken, User
from utils.tasks import  test_async
from firebase_admin import messaging
 


def test(request):
    try:
        user =User.objects.get(email="morganhezekiah111@gmail.com")
        user_token = DeviceToken.objects.get(user = user)
        n_message = messaging.Message(
        notification=messaging.Notification(
            title="title",
            body="message",
            
            
        ),
        token="c9kwrwC9SU5jsrL_CDe7ga:APA91bGb54sKz5qv_DttBx4O55TZIwTxm3BdLedl0tXKRy8FuBd5mTrWXH9TtGuo_IetrTFqJyHCxv714V-GPwa-72SmYDI101hdRyJ6h58OM4vV75bGkTY",
        data={
            "message": "message",
            "expired_data":"expired_data",
            "screen":"Referrals",
            "is_notification": "1"
        }
    )
        messaging.send(n_message)
        print("sent")
    except Exception as e:
            print(e)
    

    return render(request, "emails/message.html", {"name":"Hezekiah",
                                                   "message":"""
                                                   Thanks for downloading <b>PCN Ticket</b>! Managing parking tickets just got easier. Did you know you can cover your fines directly through the app? With a PCN Cover, we handle the hassle for you: pay your fine or even contest unfair tickets!
                                                   """
        ,"btnTitle":"Get Your Cover Now", "btnLink":"https://www.usepcn.com/#pricings"})
urlpatterns = [
    path("test/", test),
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path("pcns/", include("PCNs.urls")),
    path("vehicles/", include("vehicles.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("discount_codes/", include("discount_codes.urls")),
    path("subscription_email/", include("subscription_email.urls")),
    path("virualcards/", include("virualcards.urls")),
    path("user_notifications/", include("user_notifications.urls")),
]
