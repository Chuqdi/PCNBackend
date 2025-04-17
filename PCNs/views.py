from rest_framework.views import APIView
from rest_framework import status
from users.models import User
from users.serializers import SignUpSerializer
from utils.ResponseGenerator import ResponseGenerator
from vehicles.models import Vehicle
from .models import PCN
from datetime import timedelta
from django.utils.timezone import now
from .serializers import PCNSerializer
from django.db.models import Q
from django.conf import settings


class UpdatePCNView(APIView):
    def post(self, request, pcn_id):
        data = request.data
        pcn = PCN.objects.get(id=pcn_id)
        serializer = PCNSerializer(pcn,data=data,  partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return ResponseGenerator.response(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="PCN updated"
            )
        
        return ResponseGenerator.response(data=serializer.error_messages, message="Error updating PCN", status=status.HTTP_400_BAD_REQUEST)

class GetUserPCNsView (APIView):
    def get(self, request, user_id ):
        user = User.objects.get(id=user_id)
        pcns = PCN.objects.filter(user = user)
        return ResponseGenerator.response(
            data={
                "data":
                    PCNSerializer(pcns, many=True).data},
            message="PCNS retrieved",
            status=status.HTTP_200_OK
        )
class GetTicketsStats(APIView):
    def get(self, request):
        total_ticket = PCN.objects.all()
        pending_pcns= PCN.objects.filter(
            is_paid = False,
            is_denied = False,
        )
        approved = PCN.objects.filter(
            is_paid=True
        )
        
        return ResponseGenerator.response(data={
            "total_ticket":total_ticket.count(),
            "pending_pcns":pending_pcns.count(),
            "approved":approved.count()
        }, message="PCN stats retrieved", status=status.HTTP_200_OK)

class GetAllTickets(APIView):
    def get(self, request):
        pcns= PCN.objects.all().order_by("-id")
        searchText = request.GET.get("searchText","")
        searchCategory = request.GET.get("searchCategory", "")
        
        queryLimit = settings.QUERY_LIMIT
        page = request.GET.get("page", 1)
        requestPage = queryLimit * int(page)
        startingPage = (int(page)-1)*queryLimit
        
        if searchCategory == "Pending":
            pcns = pcns.filter(is_denied =False, is_paid=False)
        
        if searchCategory == "Approved":
            pcns = pcns.filter(is_paid=True)
        
        if searchCategory == "Denied":
            pcns = pcns.filter(is_denied=True)
        
        
        if len(searchText) > 1:
            pcns = pcns.filter(
                Q(user__email__icontains=searchText) | Q(user__full_name__icontains=searchText)
            )
            
        
        pcns = pcns[int(startingPage):requestPage]
            
        
        serializers = PCNSerializer(pcns, many=True)
        return ResponseGenerator.response(
            data={
                "data":serializers.data,
                "total":PCN.objects.all().count()
                },
            message="PCN's retrievd",
            status=status.HTTP_200_OK
        )


class GetPendingTickets(APIView):
    def get(self, request):
        pending_pcns= PCN.objects.filter(
            is_paid = False,
            is_denied = False,
        )
        
        serializers = PCNSerializer(pending_pcns, many=True)
        return ResponseGenerator.response(
            data={
                "data":serializers.data},
            message="PCN's retrievd",
            status=status.HTTP_200_OK
        )

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
        amount = request.data.get("amount")
        date_of_notice = request.data.get("date_of_notice")
        vehicle = Vehicle.objects.get(id=vehicle)
        
        pcn = PCN.objects.create(
            ticket_type=ticket_type,
            pcn=pcn,
            date_of_notice=date_of_notice,
            vehicle=vehicle,
            front_ticket_image=front_ticket_image,
            back_ticket_image=back_ticket_image,
            amount = amount,
            user=user,
        )
        user.pcn_count = user.pcn_count + 1
        user.walletCount = user.walletCount -int(amount)
        # user.date_for_next_pcn_upload = now().date() + timedelta(days=30)
        user.save()
        
        
        
        return ResponseGenerator.response(
            data={
                "data":PCNSerializer(pcn).data,
                "user":SignUpSerializer(user).data
            },
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