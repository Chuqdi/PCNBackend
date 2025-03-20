from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ChatSerializer
from utils.ResponseGenerator import ResponseGenerator
from rest_framework import status
from .models import Chat

class SendMessageFromUserView(APIView):
    def get(self, request):
        user = request.user
        chats = Chat.objects.filter(user =user)
        
        return ResponseGenerator.response(
            data=ChatSerializer(chats, many=True).data,
            message="Chats",
            status=status.HTTP_200_OK
        )
        
    def post(self, request):
        data = request.data 
        serializer = ChatSerializer(data={ **data, "user":request.user.id })
        
        if serializer.is_valid():
            serializer.save()
            
            return ResponseGenerator.response(
                data=serializer.data,
                message="User Chat sent",
                status=status.HTTP_201_CREATED
            )
            
        
        