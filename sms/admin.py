from django.contrib import admin
from .models import SMSMessage, USSDSession, USSDMenu


@admin.register(SMSMessage)
class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'message_type', 'status', 'created_at']
    list_filter = ['message_type', 'status', 'created_at']
    search_fields = ['phone_number', 'content']
    readonly_fields = ['created_at', 'delivered_at']


@admin.register(USSDSession)
class USSDSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'phone_number', 'status', 'current_step', 'created_at']
    list_filter = ['status', 'current_step', 'created_at']
    search_fields = ['session_id', 'phone_number']


@admin.register(USSDMenu)
class USSDMenuAdmin(admin.ModelAdmin):
    list_display = ['step', 'title_swahili', 'is_active']
    list_filter = ['is_active', 'step']
    search_fields = ['title', 'title_swahili']

