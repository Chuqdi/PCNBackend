
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from utils.tasks import send_email
 


def test(request):
    send_email(
        subject="Subscription confirmation",
        message="""
                                                   We have gone through your data and we see your subscription was successfully and went through. Could you refresh your browser to confirm.
                                                   """,
       recipient_list=["2006samueldhoomun1@gmail.com"],
       
        
    )
    

    return render(request, "emails/message.html", {"name":"Samuel Dhoomun",
                                                   "message":"""
                                                   We have gone through your data and we see your subscription was successfully and went through. Could you refresh your browser to confirm.
                                                   """
        ,})
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
    path("user_messages/", include("user_messages.urls")),
    path("administrators/", include("administrators.urls")),
]
