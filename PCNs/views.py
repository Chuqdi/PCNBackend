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
        data["user"] = user.id
        
        vehicle = request.data.get("vehicle")
        data["vehicle"] = Vehicle.objects.get(id=vehicle)
        
        serilizer = PCNSerializer(data=data)
        
        
        if serilizer.is_valid():
            serilizer.save()
            return ResponseGenerator.response(
                data=PCNSerializer(serilizer.instance).data,
                status=status.HTTP_201_CREATED,
                message="PCN created successfully"
            )
        return ResponseGenerator.response(
            message=serilizer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            data={}
        )
        
    def get(self, request):
        user = request.user
        PCNs = PCN.objects.filter(user =user )
        return ResponseGenerator.response(
            data=PCNSerializer(PCNs, many=True).data,
            status=status.HTTP_200_OK,
            message="PCNs retrieved successfully"
        )