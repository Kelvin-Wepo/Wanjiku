from rest_framework import serializers
from .models import VoiceSession, VoiceRecording, VoiceResponse


class VoiceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceSession
        fields = '__all__'


class VoiceRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceRecording
        fields = '__all__'


class VoiceResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceResponse
        fields = '__all__'

