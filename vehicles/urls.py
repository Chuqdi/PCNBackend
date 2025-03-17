from django.urls import path
from .views import CreateGetVehicle, EditVehicleView, GetUserVehicle


urlpatterns = [
    path("get_user_vehicles/<user_id>/", GetUserVehicle.as_view()),
    path("create_get/",CreateGetVehicle.as_view(), ),
    path("edit/<int:id>/", EditVehicleView.as_view())
]
