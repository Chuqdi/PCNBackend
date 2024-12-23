from django.shortcuts import render
from rest_framework.views import APIView
from user_notifications.models import Notification
from utils.ResponseGenerator import ResponseGenerator
from .serializers import NotificationSerializer
from rest_framework import status


class GetUserNotificationsView(APIView):
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(notifications, many=True)
        
        return ResponseGenerator.response(data =serializer.data, status=status.HTTP_200_OK, message="Get User Notifications" )