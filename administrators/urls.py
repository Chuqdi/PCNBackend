from .views import InviteAdminView, DeleteAdminView
from django.urls import path



urlpatterns = [
    path("invite/",InviteAdminView.as_view() ),
    path("invite/delete/<admin_id>/", DeleteAdminView.as_view(),), 
]
