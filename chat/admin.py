from django.contrib import admin
from .models import ChatSession, ChatMessage, SwahiliIntent


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'language', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['session_id', 'user__username']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content', 'timestamp']
    list_filter = ['message_type', 'timestamp', 'is_processed']
    search_fields = ['content', 'content_swahili']


@admin.register(SwahiliIntent)
class SwahiliIntentAdmin(admin.ModelAdmin):
    list_display = ['intent_name_swahili', 'service_category', 'is_active']
    list_filter = ['service_category', 'is_active']
    search_fields = ['intent_name', 'intent_name_swahili']

