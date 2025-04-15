from .views import GetUserNotificationsView, MarkAsRead
from django.urls import path



urlpatterns = [
    path("", GetUserNotificationsView.as_view()),
    path("<pk>/", MarkAsRead.as_view()),
    
]
