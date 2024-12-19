
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.template.loader import render_to_string
from utils.tasks import  send_email
from firebase_admin import messaging
 


def test(request):
    ## eukwKrvY40JtlQuPFHcQjI:APA91bFYGg6i0VbMljAOGBOD7AGj9y-2h6EDBc97wKKpd9rqbqyJRgxTNa52l53SYXr-xbiVJCQFVKFXdSkFgBEVTFcKGSkxEdKO354KRPtxibmgwh5ogIM
    
    
    try:

        n_message = messaging.Message(
        notification=messaging.Notification(
            title="djdjd",
            body="dfkdk",
        ),
        token="c9kwrwC9SU5jsrL_CDe7ga:APA91bGb54sKz5qv_DttBx4O55TZIwTxm3BdLedl0tXKRy8FuBd5mTrWXH9TtGuo_IetrTFqJyHCxv714V-GPwa-72SmYDI101hdRyJ6h58OM4vV75bGkTY",
    )
        messaging.send(n_message)
    except Exception as e:
        print(e)
    return render(request, "emails/message.html", {"name":"Hezekiah", "message":"dkdk"})
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
]
