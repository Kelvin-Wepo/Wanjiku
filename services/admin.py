from django.contrib import admin
from .models import GovernmentService, ServiceRequest, ServiceFAQ


@admin.register(GovernmentService)
class GovernmentServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_swahili', 'category', 'cost', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'name_swahili']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'status', 'created_at']
    list_filter = ['status', 'service', 'created_at']
    search_fields = ['user__username', 'service__name']


@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
    list_display = ['service', 'question', 'is_active']
    list_filter = ['service', 'is_active']
    search_fields = ['question', 'question_swahili']

