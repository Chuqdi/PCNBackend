from django.urls import path
from .views import CreateGetPCN


urlpatterns = [
    path("create_get/",CreateGetPCN.as_view(), )
]
