from django.urls import path
from .views import CreateGetVehicle, EditVehicleView


urlpatterns = [
    path("create_get/",CreateGetVehicle.as_view(), ),
    path("edit/<int:id>/", EditVehicleView.as_view())
]
