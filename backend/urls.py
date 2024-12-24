
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.template.loader import render_to_string
from users.models import DeviceToken, User
from users.signals import create_perodic_task
from utils.tasks import  test_async
from firebase_admin import messaging
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule
 


def test(request):
    crontab,created = CrontabSchedule.objects.get_or_create(
        minute="52",
        hour="10",
        # day_of_month=24,
        # month_of_year=12,
        # day_of_week = 52
        day_of_week='*',  # * means every day
        day_of_month='*',
        month_of_year='*'
    )
   
    
    create_perodic_task(task="send_user_second_subscription_message", crontab=crontab, arg=1)
        
    
    

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
