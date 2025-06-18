from django.urls import path
from .views import CreateGetAppeals

urlpatterns = [
    path("create_get/",CreateGetAppeals.as_view())
]
