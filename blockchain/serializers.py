from rest_framework import serializers
from .models import DocumentVerification, BlockchainTransaction, DocumentTemplate


class DocumentVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVerification
        fields = '__all__'
        read_only_fields = ['user', 'document_hash', 'created_at', 'updated_at']


class BlockchainTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockchainTransaction
        fields = '__all__'


class DocumentTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTemplate
        fields = '__all__'

