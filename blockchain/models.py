from django.db import models
from django.contrib.auth.models import User
import hashlib


class DocumentVerification(models.Model):
    """Model for document verification on blockchain"""
    DOCUMENT_TYPES = [
        ('birth_certificate', 'Birth Certificate'),
        ('id_card', 'ID Card'),
        ('passport', 'Passport'),
        ('driving_license', 'Driving License'),
        ('business_license', 'Business License'),
        ('education_certificate', 'Education Certificate'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    document_hash = models.CharField(max_length=64, unique=True)  # SHA-256 hash
    original_file = models.FileField(upload_to='documents/original/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    blockchain_tx_hash = models.CharField(max_length=66, blank=True)  # Ethereum transaction hash
    verification_data = models.JSONField(default=dict)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.document_type} - {self.user.username}"
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the document"""
        if self.original_file:
            self.original_file.seek(0)
            content = self.original_file.read()
            return hashlib.sha256(content).hexdigest()
        return None


class BlockchainTransaction(models.Model):
    """Model for blockchain transactions"""
    document_verification = models.ForeignKey(DocumentVerification, on_delete=models.CASCADE, related_name='transactions')
    tx_hash = models.CharField(max_length=66, unique=True)
    block_number = models.IntegerField(null=True, blank=True)
    gas_used = models.BigIntegerField(null=True, blank=True)
    gas_price = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"TX: {self.tx_hash[:10]}..."


class DocumentTemplate(models.Model):
    """Model for document templates"""
    name = models.CharField(max_length=100)
    name_swahili = models.CharField(max_length=100)
    document_type = models.CharField(max_length=30, choices=DocumentVerification.DOCUMENT_TYPES)
    template_file = models.FileField(upload_to='templates/')
    required_fields = models.JSONField(default=list)
    validation_rules = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name_swahili

