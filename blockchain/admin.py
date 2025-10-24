from django.contrib import admin
from .models import DocumentVerification, BlockchainTransaction, DocumentTemplate


@admin.register(DocumentVerification)
class DocumentVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'document_type', 'status', 'created_at', 'verified_at']
    list_filter = ['document_type', 'status', 'created_at']
    search_fields = ['user__username', 'document_hash']
    readonly_fields = ['document_hash', 'created_at', 'updated_at']


@admin.register(BlockchainTransaction)
class BlockchainTransactionAdmin(admin.ModelAdmin):
    list_display = ['tx_hash', 'document_verification', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['tx_hash', 'document_verification__user__username']


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ['name_swahili', 'document_type', 'is_active']
    list_filter = ['document_type', 'is_active']
    search_fields = ['name', 'name_swahili']

