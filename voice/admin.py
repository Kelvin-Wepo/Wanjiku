from django.contrib import admin
from .models import VoiceSession, VoiceRecording, VoiceResponse


@admin.register(VoiceSession)
class VoiceSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'language', 'is_active', 'created_at']
    list_filter = ['language', 'is_active', 'created_at']
    search_fields = ['session_id', 'user__username']


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ['session', 'transcript_swahili', 'confidence_score', 'created_at']
    list_filter = ['confidence_score', 'created_at']
    search_fields = ['transcript', 'transcript_swahili']


@admin.register(VoiceResponse)
class VoiceResponseAdmin(admin.ModelAdmin):
    list_display = ['session', 'text_response', 'response_type', 'created_at']
    list_filter = ['response_type', 'created_at']
    search_fields = ['text_response']

