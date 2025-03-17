from django.shortcuts import render

from users.models import User
from .serializers import AdminSerializer
from utils.ResponseGenerator import ResponseGenerator
from rest_framework import status
from .models import Admin
from rest_framework.views import APIView
from django.conf import settings
from django.db.models import Q



class DeleteAdminView(APIView):
    def delete(self, request, admin_id):
        Admin.objects.get(id=admin_id).delete()
        
        return ResponseGenerator.response(data={},status=status.HTTP_200_OK, message="Admin deleted")
        
class InviteAdminView(APIView):
    def get(self, request):
        admins = Admin.objects.all()
        searchText = request.GET.get("searchText","")
        queryLimit = settings.QUERY_LIMIT
        page = request.GET.get("page", 1)
        requestPage = queryLimit * int(page)
        startingPage = (int(page)-1)*queryLimit
        
        if len(searchText) > 2:
            admins = admins.filter(
                Q(email__icontains=searchText) | Q(name__icontains=searchText)
            )
        
        admins = admins[int(startingPage):requestPage]
        
        
        return ResponseGenerator.response(
            data={
                "data":AdminSerializer(admins, many=True).data,
                "total":Admin.objects.all().count()
                },
            message="Admin",
            status=status.HTTP_200_OK
        )
        
        
    def post(self, request):
        data  = request.data
        email = data.get("email")
        a = Admin.objects.filter(email = email)
        u = User.objects.filter(email=email)
        
        if a.exists() or u.exists():
            return ResponseGenerator.response(
                data={},
                message="User with this email already exists",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        
        serializer = AdminSerializer(data=data)
        
        
        if serializer.is_valid():
            serializer.save()
            
            return ResponseGenerator.response(
                data=serializer.data,
                message="Admin added",
                status=status.HTTP_200_OK
            )
            
        return ResponseGenerator.response(
            data={},
            status=status.HTTP_400_BAD_REQUEST,
            message="Amin was not added successfully"
        )