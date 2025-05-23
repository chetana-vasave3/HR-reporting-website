from rest_framework import serializers
from .models import Telecaller

class TelecallerSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = Telecaller
        fields = ['id', 'name', 'contact', 'mail_id', 'gender', 'experience', 'role']

    def get_role(self, obj):
        return 'Telecaller'
