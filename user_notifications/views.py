from django.shortcuts import render
from rest_framework.views import APIView
from user_notifications.models import Notification
from utils.ResponseGenerator import ResponseGenerator
from .serializers import NotificationSerializer
from rest_framework import status




class MarkAsRead(APIView):
    def post(self, request, pk):
        notification = Notification.objects.get(id=pk)
        notification.is_read = True
        notification.save()
        return ResponseGenerator.response(
            data = NotificationSerializer(notification).data,
            message="Notification read",
            status = status.HTTP_200_OK
        )
class GetUserNotificationsView(APIView):
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(notifications, many=True)
        
        return ResponseGenerator.response(data =serializer.data, status=status.HTTP_200_OK, message="Get User Notifications" )