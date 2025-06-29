from rest_framework import serializers

from vehicles.serializers import VehicleSerializer
from .models import PCN



class PCNSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(many=False)
    email = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = PCN
        fields ="__all__"
    
    
    def get_email(self, obj):
        return f"{obj.user.email}"
    
    def get_name(self, obj):
        return f"{obj.user.full_name}"