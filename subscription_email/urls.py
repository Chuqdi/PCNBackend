from .views import Subscribe, ContactUsView
from django.urls import path



urlpatterns = [
    path("subscribe/", Subscribe.as_view()),
    path("contact_us/", ContactUsView.as_view()),
]
