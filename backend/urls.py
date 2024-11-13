
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path("pcns/", include("PCNs.urls")),
    path("vehicles/", include("vehicles.urls")),
    path("subscriptions/", include("subscriptions.urls")),
]
