
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.template.loader import render_to_string
from utils.tasks import  send_email



def test(request):
    title="Your cover purchase was successful"
    body=f"""Your BASIC purchase was successful. <br /><br />
    You are covered and you can upload your first ticket 13 days from now. <br /><br />
    For more information on ticket allowances please visit our <a href='https://www.usepcn.com/terms-and-conditions'>terms and conditions.</a>"""
    
    
    message = render_to_string("emails/message.html", { "name":"Hezekiah","message":body})
    try:
        send_email(
            message=message,
            recipient_list=["morganhezekiah111@gmail.com"],
            subject=title,
            
        )
    except Exception as e:
        print(f"Error sending email: {e}")
    return render(request, "emails/message.html", {"name":"Hezekiah", "message":body})
urlpatterns = [
    path("test/", test),
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path("pcns/", include("PCNs.urls")),
    path("vehicles/", include("vehicles.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("discount_codes/", include("discount_codes.urls")),
    path("subscription_email/", include("subscription_email.urls")),
]
