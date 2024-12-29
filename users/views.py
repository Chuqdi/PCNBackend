import threading
from django.shortcuts import render
from users.models import DeviceToken, ReferalCode, User
from users.serializers import (
    ReferalCodeSerializer,
    SignUpSerializer,
)
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import logout
from utils.ResponseGenerator import ResponseGenerator
from utils.tasks import  send_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from utils.helpers import generateUserOTP, validateOTPCode
from utils.TokenGenerator import generateToken
from datetime import date





class AddUserDeviceToken(APIView):
    permission_classes = [permissions.IsAuthenticated ]
    def post(self, request):
        token = request.data.get("token")

        user = request.user

        tokenInstance, created = DeviceToken.objects.get_or_create(user = user)
        tokenInstance.token= token
        tokenInstance.save()

        
        return ResponseGenerator.response(status=status.HTTP_201_CREATED, data={}, message="Device token added successfully")




class UpdateAdminPassword(APIView):
    def put(self, request):
        try:
            user = request.user
            new_password = request.data.get("new_password")
            old_password = request.data.get("old_password")
            
            if not user.check_password(old_password):
                return ResponseGenerator.response(data={}, message="Old password is incorrect", status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(new_password):
                return ResponseGenerator.response(data={}, message="New password is same as current password", status=status.HTTP_400_BAD_REQUEST)
            
            user.password = make_password(new_password)
            user.save()
            
            serializer = SignUpSerializer(user )
           
            return ResponseGenerator.response(data=serializer.data, message="User password successfully", status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return ResponseGenerator.response(data={}, message="User not found", status=status.HTTP_404_NOT_FOUND)



class EditUserWithProfileImageView(APIView):
    def put(self, request):
        try:
            user = request.user
            user.full_name = request.data.get('full_name')
            user.email = request.data.get('email')
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                user.profile_image = profile_image
            user.save()
            
            serializer = SignUpSerializer(user )
           
            return ResponseGenerator.response(data=serializer.data, message="User updated successfully", status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return ResponseGenerator.response(data={}, message="User not found", status=status.HTTP_404_NOT_FOUND)



class UsersStatsView(APIView):
    def get(self, request, *args, **kwargs):
        today = date.today()
        users = User.objects.all()
        total_users = users.filter(is_superuser=False)
        active_users = total_users.filter(is_active=True)
        suspended_users = total_users.filter(is_active=False)
        joined_today = total_users.filter(date_joined__date=today)
        
        return ResponseGenerator.response(
            data={
                "total_users": total_users.count(),
                "active_users": active_users.count(),
                "suspended_users": suspended_users.count(),
                "joined_today":joined_today.count(),
            },
            message="Stats for users",
            status=status.HTTP_200_OK
        )
        

class EditUserView(APIView):
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.full_name = request.data.get('full_name')
            user.email = request.data.get('email')
            user.phone_number = request.data.get('phone_number')
            user.home_address = request.data.get('home_address')
            user.save()
            
            serializer = SignUpSerializer(user )
           
            return ResponseGenerator.response(data=serializer.data, message="User updated successfully", status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return ResponseGenerator.response(data={}, message="User not found", status=status.HTTP_404_NOT_FOUND)


class ToggleUserActiveState(APIView):
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            user.save()
            return ResponseGenerator.response(data={}, message="User status toggled successfully", status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return ResponseGenerator.response(data={}, message="User not found", status=status.HTTP_404_NOT_FOUND)


     

class GetPostAdministrators(APIView):
    def get(self, request):
        queryLimit = settings.QUERY_LIMIT
        page = request.GET.get("page", 1)
        requestPage = queryLimit * int(page)
        startingPage = (int(page)-1)*queryLimit
        searchQuery = request.GET.get("searchQuery","")
        user = User.objects.filter(Q(email__icontains=searchQuery) |
                Q(full_name__icontains=searchQuery) |
                Q(phone_number__icontains=searchQuery)).filter(is_superuser =False)[int(startingPage):requestPage]
        allUser = User.objects.filter(is_superuser =False)
        serializer = SignUpSerializer(user, many=True)
        return ResponseGenerator.response(data={
            "data":serializer.data, "total_count":allUser.count()}, message="Users retrieved successfully", status=status.HTTP_200_OK)





class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        s = SignUpSerializer(data=request.data)
        email = request.data.get("email")
        if User.objects.filter(email = email).exists():
            return ResponseGenerator.response(
                data={},
                    message="User with this email already exists",
                status=status.HTTP_400_BAD_REQUEST
            )



        if s.is_valid():
            s.save()
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            



            message = render_to_string("emails/welcome.html", { "name":f"{first_name} {last_name}"})
            t = threading.Thread(target=send_email, args=(f"Welcome {first_name}", message,[email]))
            t.start()

            user = User.objects.get(email=email)
            user.is_active= True
            user.save()


            
            responseData = {"data":s.data, "token":user.auth_token.key}
            return ResponseGenerator.response(data=responseData, message="User  registered successfully", status=status.HTTP_201_CREATED)
  
            
        return ResponseGenerator.response(message= s.errors,status=status.HTTP_400_BAD_REQUEST)



class ActivateUserEmail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token, uidb64):
        try:
            uuid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uuid)
        except Exception as e:
            user = None

        if user and generateToken.check_token(user, token):
            user.is_active = True
            user.save()

            return render(
                request,
                "notification.html",
                {
                    "message": "User account activated successfully, please return to the login to continue process.",
                    "user":user
                },

            )

        return render(
            request,
            "notification.html",
            {"message": "Sorry, there was an error activating your account"},
        )



class LoginUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = User.objects.filter(email__iexact=request.data.get("email"))
        print(user)
        isAdmin = request.data.get("isAdmin", False)
        if user.exists() and not user[0].is_active:
            return ResponseGenerator.response(
                message="Sorry User account is not activated",
                data={},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = user[0]
        checking_password = check_password(request.data.get("password"), user.password)

        if isAdmin and user and not user.is_superuser:
            return ResponseGenerator.response(
                    message="Sorry User is not admin",
                    data={},
                status=status.HTTP_400_BAD_REQUEST,
            )



        if checking_password:
            return ResponseGenerator.response(
                data={"data": SignUpSerializer(user).data, "token": user.auth_token.key},
                message="User logged in successfully",
                status=status.HTTP_200_OK,
            )
        return ResponseGenerator.response(
            data={},
            message= "User Credentials are not correct",
            status=status.HTTP_404_NOT_FOUND,
        )


class UserMe(APIView):
    def get(self, request, id):
        user = User.objects.filter(id=id)

        if user.exists():
            return Response(
                data={"message": "User with this ID does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data={
                "data": SignUpSerializer(instance=user[0]),
                "message": "User retrieved successfully",
            },
            status=status.HTTP_200_OK,
        )

class DeleteUserWithEmail(APIView):
    permission_classes=[permissions.AllowAny]
    def delete(self, request, email):
        try:
            user = User.objects.get(email=email)
            user.delete()
            return Response(
                data={
                    "message": "User deleted successfully",
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist as e:
            return Response(
                data={
                    "message": "User with this email does not exist",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserMeAuth(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
       
        return ResponseGenerator.response(
            data=SignUpSerializer(user).data,
            message="User authenticated",
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        id = request.user.id
        user = User.objects.get(id=id).delete()

        return Response(
            data={
                "messgae": "User Deleted Successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutUser(APIView):

    def post(self, request):
        logout(request=request)
        return Response(data={"message": "User Logged Out Successfully"})


class GetUserReferalCode(APIView):
  
    def get(self, request):
        r = ReferalCode.objects.get(user=request.user)
        return Response(data=ReferalCodeSerializer(r).data, status=status.HTTP_200_OK)




class ForgotPasswordRequest(APIView):
    permission_classes = [permissions.AllowAny ]
    def post(self, request):
        email = request.data.get("email")


        user = User.objects.filter(email= email)

        if not user.exists():
            return ResponseGenerator.response(
            data={
            },
            message= "Sorry, User with this email does not exist",
            status=status.HTTP_400_BAD_REQUEST,
        )
        

        c = generateUserOTP(user[0].email)
        emailMessage =f"We received a request to reset the password for your account associated with this email address. If you didn't request a password reset, please ignore this email. To reset your password, please use the code below \n\n {c} "
        message = render_to_string("emails/message.html", { "message":emailMessage, "name":f"{user[0].full_name}"})
        t = threading.Thread(target=send_email, args=("Your Password reset", message,[email]))
        t.start()
        


        
        return ResponseGenerator.response(
            message=f"Forgot Password code sent to email.",
            data=SignUpSerializer(user[0]).data,
            status=status.HTTP_200_OK,
        )


class ContinueForgotOTPPassword(APIView):
    permission_classes = [ permissions.AllowAny ]
    def post(self, request):
        code = request.data.get("code")
        validatingOTP = validateOTPCode(code)
        if not validatingOTP.get("type"):
            return Response(
            data={
                "error": validatingOTP.get("message"),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


        user = validatingOTP.get("code").user
        

        return ResponseGenerator.response(
            data=SignUpSerializer(user).data,
            message= "User password updated successfully",
            status=status.HTTP_200_OK,
        )

class CompletePasswordReset(APIView):
    permission_classes = [ permissions.AllowAny ]
    def post(self, request):
        password = request.data.get("password")

        if not password:
            return Response(data ={ "message":"Please enter your password"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_model().objects.get(id = request.data.get("user_id"))
        user.set_password(password)
        user.save()

        return ResponseGenerator.response(
            data=SignUpSerializer(user).data,
            message="User password updated",
            status=status.HTTP_202_ACCEPTED)

class GetUserWithID(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            return Response(data={"data": SignUpSerializer(user).data,"message":"User retrieved successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data ={ "message":"User with this ID does not exist"}, status=status.HTTP_400_BAD_REQUEST)
class UpdateUserPassword(APIView):
    def post(self, request):
        old_password = request.data.get("old_password")
        password = request.data.get("password")


        

        if not password:
            return Response(data ={ "message":"Please enter your password"}, status=status.HTTP_400_BAD_REQUEST)
        

        
        user = get_user_model().objects.get(id = request.user.id)
        

        if not user.check_password(old_password):
            return Response(data ={ "message":"Your old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        if  user.check_password(password):
            return Response(data ={ "message":"Password must not be the same as the old one"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()




        
        return Response(data={
            "message":"User password updated",
        }, status=status.HTTP_202_ACCEPTED)
        
        

class UpdateUserBasicInformation(APIView):
    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        business_category = request.data.get("business_category")


        if not first_name:
            return Response(data ={ "message":"Please enter your first name"}, status=status.HTTP_400_BAD_REQUEST)
        


        if not last_name:
            return Response(data ={ "message":"Please enter your last name"}, status=status.HTTP_400_BAD_REQUEST)
        

        if not email:
            return Response(data ={ "message":"Please enter your email"}, status=status.HTTP_400_BAD_REQUEST)
        

        if not phone_number:
            return Response(data ={ "message":"Please enter your phone number"}, status=status.HTTP_400_BAD_REQUEST)
        

        
        user =  User.objects.get(id = request.user.id)
        user.email = email
        user.phone_number = phone_number
        user.first_name= first_name
        user.last_name = last_name
        if business_category:
            user.business_category = business_category

        user.save()
        


       
        return Response(data={
            "message":"User profile updated",
            "user":SignUpSerializer(user).data
        },
        status=status.HTTP_201_CREATED)
     


class DeleteAccount(APIView):
    def delete(self, request):
        user = request.user
        user = User.objects.get(email=user.email)
        user.delete()

        return Response(data={
            "message":"User account deleted successfully"
        }, status=status.HTTP_202_ACCEPTED)
    



class UpdateProfileImage(APIView):
    def patch(self, request):
        image = request.FILES.get("profile_image")
        user = request.user
        user.profile_image = image
        user.save()

        return Response(data={
            "message":"Profile image updated successfully",
            "user":SignUpSerializer(user).data,
        }, status=status.HTTP_202_ACCEPTED)
    


class GetUserTokenWithEmail(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self, request,email, *args, **kwargs):
        try:
            user = User.objects.get(email=email)
            return Response(data={
                "token":user.auth_token.key,
                "message":"User token found",
            })
        except:
            return Response(data ={ "message":"User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)