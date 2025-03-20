from .views import SendMessageFromUserView
from django.urls import path


urlpatterns = [
    path("send_or_get_user/", SendMessageFromUserView.as_view()),
]