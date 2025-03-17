from django.shortcuts import render
from utils.ResponseGenerator import ResponseGenerator
from users.models import User
from rest_framework import status
from rest_framework.views import APIView
from .models import UserMessage



class SendUserMessage(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        user = User.objects.get(id = user_id)
        as_mobile_notification = request.data.get("as_mobile_notification")
        as_email = request.data.get("as_email")
        title = request.data.get("title")
        content = request.data.get("content")
        
        UserMessage.objects.create(
            title=title,
            as_mobile_notification = as_mobile_notification,
            as_email = as_email,
            user = user,
            content = content
        )
        return ResponseGenerator.response(
            data={
                "message":"Email sent"},
            message="User message sent",
            status= status.HTTP_200_OK
        )
        
        
        
        

