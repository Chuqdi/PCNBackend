from .views import SendUserMessage
from django.urls import path


urlpatterns = [
    path("send_message/", SendUserMessage.as_view(),)
]
