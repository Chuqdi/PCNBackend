
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
        token="d2u_tcdNRE4Tt7arPYN5dn:APA91bEBbXEDjdaIue5rMPfY8OfMG4fJkXb6hCVhiXpTPkG8sI_XJYhhgrxe6gXoJAaYADcPlm0vV6vcnCH3Pm8gUZA4SvVgijD7X_whrBv3A9c1N0Y2DzY",
    )
        messaging.send(n_message)
        print("sent")
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
