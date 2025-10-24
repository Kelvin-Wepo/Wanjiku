from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    """Model for user documents"""
    DOCUMENT_TYPES = [
        ('birth_certificate', 'Birth Certificate'),
        ('id_card', 'ID Card'),
        ('passport', 'Passport'),
        ('driving_license', 'Driving License'),
        ('business_license', 'Business License'),
        ('education_certificate', 'Education Certificate'),
        ('marriage_certificate', 'Marriage Certificate'),
        ('death_certificate', 'Death Certificate'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    title_swahili = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    file_hash = models.CharField(max_length=64, blank=True)  # SHA-256 hash
    description = models.TextField(blank=True)
    description_swahili = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class DocumentCategory(models.Model):
    """Model for document categories"""
    name = models.CharField(max_length=100)
    name_swahili = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    description_swahili = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Document Categories'
    
    def __str__(self):
        return self.name_swahili


class DocumentTemplate(models.Model):
    """Model for document templates"""
    name = models.CharField(max_length=100)
    name_swahili = models.CharField(max_length=100)
    document_type = models.CharField(max_length=30, choices=Document.DOCUMENT_TYPES)
    template_file = models.FileField(upload_to='templates/')
    instructions = models.TextField()
    instructions_swahili = models.TextField()
    required_fields = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name_swahili

