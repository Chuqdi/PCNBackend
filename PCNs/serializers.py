from rest_framework.serializers import ModelSerializer

from vehicles.serializers import VehicleSerializer
from .models import PCN



class PCNSerializer(ModelSerializer):
    vehicle = VehicleSerializer(many=False)
    class Meta:
        model = PCN
        fields ="__all__"