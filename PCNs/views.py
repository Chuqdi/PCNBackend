from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from utils.ResponseGenerator import ResponseGenerator
from vehicles.models import Vehicle
from .models import PCN
from .serializers import PCNSerializer



class CreateGetPCN(APIView):
    def post(self, request):
        data = request.data
        user = request.user
        
        vehicle = request.data.get("vehicle")
        pcn = request.data.get("pcn")
        date_of_notice = request.data.get("date_of_notice")
        front_ticket_image = request.data.get("front_ticket_image")
        back_ticket_image = request.data.get("back_ticket_image")
        ticket_type = request.data.get("ticket_type")
        date_of_notice = request.data.get("date_of_notice")
        vehicle = Vehicle.objects.get(id=vehicle)
        
        pcn = PCN.objects.create(
            ticket_type=ticket_type,
            pcn=pcn,
            date_of_notice=date_of_notice,
            vehicle=vehicle,
            front_ticket_image=front_ticket_image,
            back_ticket_image=back_ticket_image,
            user=user,
        )
        
        
        return ResponseGenerator.response(
            data=PCNSerializer(pcn).data,
            status=status.HTTP_201_CREATED,
            message="PCN created successfully"
        )
        
        
    def get(self, request):
        user = request.user
        PCNs = PCN.objects.filter(user =user )
        return ResponseGenerator.response(
            data=PCNSerializer(PCNs, many=True).data,
            status=status.HTTP_200_OK,
            message="PCNs retrieved successfully"
        )