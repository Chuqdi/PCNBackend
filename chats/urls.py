from .views import GetAdminUnReadMessageForSingleMessage, GetAdminUserMessages, GetAllAdminUnreadMessages, MarkChatAsRead, SendMessageFromUserView, GetMessageSetForAdmin
from django.urls import path


urlpatterns = [
    path("send_or_get_user/", SendMessageFromUserView.as_view()),
    path("send_or_get_admin/", GetMessageSetForAdmin.as_view()),
    path("admin_unread_messages/", GetAllAdminUnreadMessages.as_view(),),
    path("get_admin_users_messages/<user_id>/", GetAdminUserMessages.as_view(),),
    path("single_user_unread_count/<user_id>/",GetAdminUnReadMessageForSingleMessage.as_view(),),
    path("mark_chat_as_read/<id>/", MarkChatAsRead.as_view(),)
]