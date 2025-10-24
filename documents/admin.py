from django.contrib import admin
from .models import Document, DocumentCategory, DocumentTemplate


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['user', 'title_swahili', 'document_type', 'is_verified', 'created_at']
    list_filter = ['document_type', 'is_verified', 'created_at']
    search_fields = ['user__username', 'title', 'title_swahili']


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name_swahili', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'name_swahili']


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ['name_swahili', 'document_type', 'is_active']
    list_filter = ['document_type', 'is_active']
    search_fields = ['name', 'name_swahili']

