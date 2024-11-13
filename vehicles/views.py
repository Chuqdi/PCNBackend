from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from utils.ResponseGenerator import ResponseGenerator
from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer


class EditVehicleView(APIView):
    def put(self, request, id):
        vehicle = Vehicle.objects.get(id=id)
        if vehicle:
            data = request.data
            serializer = VehicleSerializer(vehicle, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return ResponseGenerator.response(
                    data=serializer.data,
                    status=status.HTTP_200_OK,
                    message="Vehicle updated successfully"
                )
            return ResponseGenerator.response(
                message=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                data={}
            )
        return ResponseGenerator.response(
            message="Vehicle not found",
            status=status.HTTP_404_NOT_FOUND,
            data={}
        )

class CreateGetVehicle(APIView):
    def post(self, request):
        data = request.data
        user = request.user
        data["user"] = user.id
        
        vehicle_number = request.data.get("vehicle_number")
        
        if Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
            return ResponseGenerator.response(
                message= "Vehicle with this number already exists in our system",
                status=status.HTTP_400_BAD_REQUEST,
                data={}
            )
       
        
        serilizer = VehicleSerializer(data=data)
        
        if serilizer.is_valid():
            serilizer.save()
            return ResponseGenerator.response(
                data=VehicleSerializer(serilizer.instance).data,
                status=status.HTTP_201_CREATED,
                message="Vehicle created successfully"
            )
        print(serilizer.errors)
        return ResponseGenerator.response(
            message=serilizer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            data={}
        )
        
    def get(self, request):
        user = request.user
        vehicles = Vehicle.objects.filter(user =user )
        return ResponseGenerator.response(
            data=VehicleSerializer(vehicles, many=True).data,
            status=status.HTTP_200_OK,
            message="Vehicles retrieved successfully"
        )