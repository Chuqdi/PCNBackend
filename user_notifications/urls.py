from .views import GetUserNotificationsView
from django.urls import path



urlpatterns = [
    path("", GetUserNotificationsView.as_view())
]
