from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ChatSerializer
from utils.ResponseGenerator import ResponseGenerator
from rest_framework import status
from .models import Chat
from django.db.models import Max, Subquery, OuterRef 
from users.models import User



class MarkChatAsRead(APIView):
    def post(self, request, id):
        chat = Chat.objects.get(id = id)
        chat.is_read =True
        chat.save()
        
        return ResponseGenerator.response(
            data= ChatSerializer(chat).data,
            message="Chat Updated",
            status=status.HTTP_200_OK
        )

class GetAllAdminUnreadMessages(APIView):
    def get(self, request):
        chats = Chat.objects.filter(
            sent = True,
            is_read = False
        )
        
        return ResponseGenerator.response(
            data=chats.count(),
            status=status.HTTP_200_OK,
            message="Unread chats"
        )

class GetAdminUserMessages(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        chats = Chat.objects.filter(
            user = user,
        )
        
        return ResponseGenerator.response(
            data=ChatSerializer(chats, many=True).data,
            status=status.HTTP_200_OK,
            message="Messages retireved"
        )
        
        

class GetAdminUnReadMessageForSingleMessage(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        chats = Chat.objects.filter(
            user = user,
            sent=True,
            is_read=False
        )
        
        return ResponseGenerator.response(
            data=chats.count(),
            status=status.HTTP_200_OK,
            message="Messages count retireved"
        )
class GetMessageSetForAdmin(APIView):
    def get(self, request):
        latest_messages = Chat.objects.values('user').annotate(
            latest_id=Max('id')
        ).values_list('latest_id', flat=True)
        user_messages = Chat.objects.filter(id__in=latest_messages)
        
        serializer = ChatSerializer(
            user_messages,
            many=True
        )
        
        return ResponseGenerator.response(
            data=serializer.data,
            message="Admin messages returned",
            status=status.HTTP_200_OK
        )
        
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
        is_admin = request.data.get("is_admin", False)
        user = request.date.get("user")
        serializer = ChatSerializer(data={ **data, "user":user if is_admin else request.user.id, "sent": True if not is_admin else False })
        
        if serializer.is_valid():
            serializer.save()
            
            return ResponseGenerator.response(
                data=serializer.data,
                message="User Chat sent",
                status=status.HTTP_201_CREATED
            )
            
        
        