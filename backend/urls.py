
from datetime import datetime
import threading
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from users.models import User
from utils.helpers import send_to_zapier
from utils.tasks import send_email
from django.template.loader import render_to_string
from PCNs.models import PCN
from django_celery_beat.models import CrontabSchedule, ClockedSchedule,PeriodicTask
from datetime import datetime, timedelta
import json


def test(request):
    target_datetime = datetime.now() + timedelta(hours=0.01666666666)
    
        
        ### FIRST MESSAGE 
    clocked_schedule = ClockedSchedule.objects.create(
        clocked_time=target_datetime
    )
    instance = User.objects.get(email="morganhezekiah111@gmail.com")
    task = PeriodicTask.objects.create(
            clocked=clocked_schedule,
            task= f'utils.tasks.send_notification_email',
            name="test_task"+str(datetime.now().second),
            one_off=True,
            kwargs=json.dumps({
                "user":instance.id,
                "template":"first_reminder.html",
                "subject":"test",
                "plan":False
            })
        )
    print(task)
    return render(request, "emails/welcome.html", { "name":"Hezekiah", })
    
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
