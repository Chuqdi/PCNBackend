from django.urls import path
from .views import CreateGetPCN, GetAllTickets, GetPendingTickets, GetTicketsStats, GetUserPCNsView, UpdatePCNView


urlpatterns = [
    path('get_user_pcns/<user_id>/', GetUserPCNsView.as_view(),),
    path("get_all_pcns/", GetAllTickets.as_view(),),
    path("pcn_stats/", GetTicketsStats.as_view(),),
    path("get_pending_pcn/", GetPendingTickets.as_view()),
    path("create_get/",CreateGetPCN.as_view(), ),
    path("update_pcn/<pcn_id>/", UpdatePCNView.as_view(),),
]
