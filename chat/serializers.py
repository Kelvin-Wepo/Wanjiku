from rest_framework import serializers
from .models import ChatSession, ChatMessage, SwahiliIntent


class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'


class SwahiliIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwahiliIntent
        fields = '__all__'

