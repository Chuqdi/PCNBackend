from django.shortcuts import render
from .models import SubscriptionEmail, ContactUsEmail
from rest_framework.views import APIView
from rest_framework import status
from utils.ResponseGenerator import ResponseGenerator
from rest_framework import permissions




class ContactUsView(APIView):
    permission_classes = [ permissions.AllowAny ]
    def post(self, request):
        first_name = request.data.get('first_name')
        email = request.data.get('email')
        message = request.data.get('message')
        last_name = request.data.get('last_name')
        ContactUsEmail.objects.create(first_name=first_name,last_name=last_name,email=email, message=message)
        
        return ResponseGenerator.response(data={"status":True}, status=status.HTTP_201_CREATED, message="Contact Us email sent successfully")
        

class Subscribe(APIView):
    permission_classes=[permissions.AllowAny]
    def post(slf, request):
        email = request.GET.get('email')
        
        if SubscriptionEmail.objects.filter(email=email).exists():
            return ResponseGenerator.response(
                data={}, status=status.HTTP_400_BAD_REQUEST,
                message="Email already subscribed"
            )
        
        SubscriptionEmail.objects.create(email=email)
        
        
        return ResponseGenerator.response(status=status.HTTP_201_CREATED,data={"status":True}, message="User subscription was successful")
