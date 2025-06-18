
import threading
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from utils.tasks import send_email
from utils.tasks import send_email
from django.template.loader import render_to_string
from PCNs.models import PCN

def test(request):
    ticket = PCN.objects.first()
    message = render_to_string("emails/ticket_denied.html", { "name":"m","ticket":ticket})
    t = threading.Thread(target=send_email, args=(f"Your PCN status update", message,["morganhezekiah111@gmail.com"]))
    t.start()
    

    return render(request, "emails/ticket_denied.html", {"name":"Hezekia Morgan",
                                                   "ticket":ticket
        ,})
urlpatterns = [
    path("test/", test),
    path('admin/', admin.site.urls),
    path("appeals/", include("appeals.urls")),
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
    path("chats/", include("chats.urls")),
]
