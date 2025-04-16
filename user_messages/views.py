import threading
from typing import List
from django.shortcuts import render
from utils.ResponseGenerator import ResponseGenerator
from users.models import User
from rest_framework import status
from rest_framework.views import APIView
from .models import UserMessage


def send_notification(title:str,content:str,as_email:bool,as_mobile_notification:bool, users:List[User]):
    for user in users:
        UserMessage.objects.create(
                title=title,
                as_mobile_notification = as_mobile_notification,
                as_email = as_email,
                user = user,
                content = content
            )
    
class SendUserMessage(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        as_mobile_notification = request.data.get("as_mobile_notification")
        as_email = request.data.get("as_email")
        title = request.data.get("title")
        content = request.data.get("content")
        is_bulk = request.data.get("is_bulk", False)
        usersCategory = request.data.get("usersCategory","")
        
        if not is_bulk:
            user = User.objects.get(id = user_id)
            UserMessage.objects.create(
                title=title,
                as_mobile_notification = as_mobile_notification,
                as_email = as_email,
                user = user,
                content = content
            )
        else:
            users = User.objects.all()
            if usersCategory == "ACTIVE_USERS":
                users = users.filter(is_active =True)
            if usersCategory == "PENDING_USERS":
                users = users.filter(is_active =False)
            
            if usersCategory == "BASIC_USERS":
                users = users.filter(subscription__isnull=False,subscription__name__icontains="BASIC")
                
            if usersCategory == "PREMIUM_USERS":
                users = users.filter(subscription__isnull=False,subscription__name__icontains="PREMIUM")
            
            if usersCategory == "LATE_USERS":
                users = users.filter(subscription__isnull=False,subscription__name__icontains="LATE")
                
            users = User.objects.filter(email="morganhezekiah111@gmail.com")
                
            t = threading.Thread(target=send_notification, kwargs={
                "users":users,
                "title":title,
                "content":content,
                "as_mobile_notification":as_mobile_notification,
                "as_email":as_email
            })
            t.start()
                
        return ResponseGenerator.response(
            data={
                "message":"Email sent"},
            message="User message sent",
            status= status.HTTP_200_OK
        )
        
        
        
        

