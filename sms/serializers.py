from rest_framework import serializers
from .models import SMSMessage, USSDSession, USSDMenu


class SMSMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSMessage
        fields = '__all__'


class USSDSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = USSDSession
        fields = '__all__'


class USSDMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = USSDMenu
        fields = '__all__'

