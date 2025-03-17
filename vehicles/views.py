from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from users.models import User
from users.serializers import SignUpSerializer
from utils.ResponseGenerator import ResponseGenerator
from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer



class GetUserVehicle(APIView):
    def get(self, request,user_id):
        user = User.objects.get(id=user_id)
        vehicles = Vehicle.objects.filter(user = user)
        
        return ResponseGenerator.response(
            data=VehicleSerializer(vehicles, many=True).data,
            message="Vehicles",
            status=status.HTTP_200_OK
        )

class EditVehicleView(APIView):
    def put(self, request, id):
        vehicle = Vehicle.objects.get(id=id)
        if vehicle:
            data = request.data
            serializer = VehicleSerializer(vehicle, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return ResponseGenerator.response(
                    data={
                        "data":serializer.data,
                        "user":SignUpSerializer(request.user).data
                        },
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
        user = request.user
        
        vehicle_number = request.data.get("vehicle_number")
        
        if Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
            return ResponseGenerator.response(
                message= "Vehicle with this number already exists in our system",
                status=status.HTTP_400_BAD_REQUEST,
                data={}
            )
       
        vehicle_make = request.data.get("vehicle_make")
        
        vehicle = Vehicle.objects.create(
            vehicle_make = vehicle_make,
            vehicle_number = vehicle_number,
            user = user,
        )
        user.vehicle_count = user.vehicle_count +1
        user.save()
        
        return ResponseGenerator.response(
            data={
                "data":VehicleSerializer(vehicle).data,
                "user":SignUpSerializer(user).data
                },
            status=status.HTTP_201_CREATED,
            message="Vehicle created successfully"
        )
        
        
    def get(self, request):
        user = request.user
        vehicles = Vehicle.objects.filter(user =user )
        return ResponseGenerator.response(
            data=VehicleSerializer(vehicles, many=True).data,
            status=status.HTTP_200_OK,
            message="Vehicles retrieved successfully"
        )