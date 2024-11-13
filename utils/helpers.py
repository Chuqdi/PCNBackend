import threading
from django.utils import timezone
from utils.randomString import GenerateRandomString
from users.models import  User, UserEmailActivationCode
from datetime import timedelta
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from utils.TokenGenerator import generateToken
from django.conf import settings
from firebase_admin import messaging
from django.conf import settings
import requests
from datetime import datetime
from django.conf import settings




def validate_ios_receipt(receipt_data):
    PRODUCTION_URL = "https://buy.itunes.apple.com/verifyReceipt"  # Production URL
    SANDBOX_URL = "https://sandbox.itunes.apple.com/verifyReceipt"  # Sandbox URL

    data = {
        'receipt-data': receipt_data,
        'password': settings.IOS_PAYMENT_SHARED_SECRET,  # Your App's shared secret
        'exclude-old-transactions': True  # Optional, excludes old transactions
    }
    
    # First attempt with production URL
    response = requests.post(PRODUCTION_URL, json=data)
    
    if response.status_code == 200:
        apple_response = response.json()
        
        if apple_response['status'] == 0:
            expiration_time = apple_response['receipt'].get('expires_date')
            
            if expiration_time:
                # Check if receipt is expired
                expiration_date = datetime.fromtimestamp(int(expiration_time) / 1000)
                if expiration_date < datetime.now():
                    return {
                        'status': 'error',
                        'message': 'Receipt is expired.'
                    }
            
            return {
                'status': 'success',
                'receipt': apple_response['receipt'],
                'latest_receipt_info': apple_response.get('latest_receipt_info', []),
            }
        
        # Check for specific error indicating sandbox receipt
        if apple_response['status'] == 21007:
            # Retry validation with sandbox URL
            response = requests.post(SANDBOX_URL, json=data)
            
            if response.status_code == 200:
                apple_response = response.json()
                
                if apple_response['status'] == 0:
                    expiration_time = apple_response['receipt'].get('expires_date')
                    
                    if expiration_time:
                        # Check if receipt is expired
                        expiration_date = datetime.fromtimestamp(int(expiration_time) / 1000)
                        if expiration_date < datetime.now():
                            return {
                                'status': 'error',
                                'message': 'Receipt is expired.'
                            }
                    
                    return {
                        'status': 'success',
                        'receipt': apple_response['receipt'],
                        'latest_receipt_info': apple_response.get('latest_receipt_info', []),
                    }
        
        # If not a sandbox receipt or expired receipt, return the error
        return {
            'status': 'error',
            'message': f"Apple verification failed: {apple_response.get('status', 'Unknown error')}"
        }
    
    else:
        return {
            'status': 'error',
            'message': f"Failed to connect to Apple's server. Status code: {response.status_code}"
        }





def send_email_here( subject, message, recipient_list, ):
    message = EmailMessage(subject, message,  settings.DEFAULT_FROM_EMAIL,recipient_list)
    message.content_subtype = 'html' 
    message.send()


def send_fcm_message(token, title, body):
    print("Toke "+token)
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token.strip(),
    )
    response = messaging.send(message)


def notifyRole(test):
    roles = Role.objects.all()
    for role in roles.iterator():
        user = role.user
        email = user.email
        message = "Congrats, an employer viewed your job role."
        if user.subscription == "FREE":
            message = f"{message} Please subscribe to a higher plan to see employers details"
        t = threading.Thread(target=send_email_here, args=("Account Notification", message, [email]))
        t.start()

        user_tokens = DeviceToken.objects.filter(user = user)

        for token in user_tokens.iterator():
            send_fcm_message(token.token, "Account Notification", message)
        role.view_count = int(role.view_count) + 1
        role.save()



    

def formatResumeDownloadLink(role_id):
    path = f"{settings.BACKEND_URL}api/v1/roles/download_role_data/{role_id}/"
    return path
     

def generateUserOTP(email):
    user = User.objects.get(email=email)
    code = GenerateRandomString.randomStringGenerator(6).upper()
    c = UserEmailActivationCode.objects.create(user=user, code =code)
    return code


def generateSecureEmailCredentials(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = generateToken.make_token(user)

    return {"uidb64": uidb64, "token": token}




def validateOTPCode(code):
    
        c = UserEmailActivationCode.objects.filter(code = code)

        if not c.exists():
            return {
                "message":"OTP does not exist",
                "type":False
            }

        code = c[0]
        if (code.date_created + timedelta(minutes=30)) < timezone.now():
            code.delete()
            return {
                "message":"OTP has expired",
                "type":False,
            }
        code.delete()

        return  {
                "message":"OTP is valid",
                "type":True,
                "code":code
            }







