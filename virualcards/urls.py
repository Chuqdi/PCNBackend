from django.urls import path
from .views import CreateVirtualCard


urlpatterns = [
    path("create/", CreateVirtualCard.as_view())
]
