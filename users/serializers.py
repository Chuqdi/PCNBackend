from users.models import ReferalCode, User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.conf import settings
from utils.randomString import GenerateRandomString
from django.conf import settings
import stripe



def checkUserCodeExist():
    code = GenerateRandomString.randomAlhanumeric(6)
    if ReferalCode.objects.filter(code=code).exists():
        checkUserCodeExist()
    return code


class ReferalCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferalCode
        fields=[
            "code"
        ]


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length =8)
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "full_name",
            "is_new",
            "is_active",
            "phone_number",
            "referalCode",
            "refered_by_code",
            "is_superuser",
            "profile_image",
            "home_address",
            "is_staff",
            "subscription"
        ]



    def validate(self, attrs):
        if User.objects.filter(email=attrs.get("email")).exists():
            raise ValidationError("User email already taken")

        return super().validate(attrs)
    
    def create(self, validated_data):
        stripe.api_key = settings.STRIPE_SECRET_KEY 
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        referalCode =checkUserCodeExist()
        r =ReferalCode.objects.create(user=user, code = referalCode)
        customer = stripe.Customer.create(
        name=user.full_name,
        email=user.email,
        )
        user.stripe_id = customer.id
        Token.objects.create(user=user)
        user.save()
        
        return user
 