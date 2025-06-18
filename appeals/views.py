from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.views import APIView
from utils.ResponseGenerator import ResponseGenerator
from .serializers import AppealSerializer
from .models import Appeal
from rest_framework import status

class CreateGetAppeals(APIView):
    def get(self, request):
        appeals = Appeal.objects.filter(user = request.user)
        return ResponseGenerator.response(
            data=AppealSerializer(appeals, many=True).data,
            message="Appeals",
            status=status.HTTP_200_OK
        )
    def post(self, request):
        date_of_notice = request.data.get("date_of_notice")
        ticket_type = request.data.get("ticket_type")
        pcn = request.data.get("pcn")
        front_ticket_image = request.data.get("front_ticket_image")
        back_ticket_image = request.data.get("back_ticket_image")
        registeration_number =  request.data.get("registeration_number")
        
        
        
        
        appeal = Appeal.objects.create(
            ticket_type=ticket_type,
            pcn =pcn,
            front_ticket_image = front_ticket_image,
            back_ticket_image = back_ticket_image,
            registeration_number=registeration_number,
            date_of_notice =date_of_notice,
            user = request.user
        )
        
        serializer = AppealSerializer(
            appeal
        )
        
        return ResponseGenerator.response(
            data=serializer.data,
            status=status.HTTP_200_OK,
            message="Appeal created"
        )