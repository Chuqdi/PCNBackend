from .models import Chat
from rest_framework import serializers

class ChatSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = "__all__"
        
    def get_email(self, obj):
        if obj.user:
            return f"{obj.user.email}"