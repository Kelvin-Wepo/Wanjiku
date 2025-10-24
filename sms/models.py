from django.db import models
from django.contrib.auth.models import User


class SMSMessage(models.Model):
    """Model for SMS messages"""
    MESSAGE_TYPES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]
    
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    phone_number = models.CharField(max_length=20)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    content_swahili = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"SMS to {self.phone_number}: {self.content[:50]}"


class USSDSession(models.Model):
    """Model for USSD sessions"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]
    
    session_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    current_step = models.CharField(max_length=50, default='welcome')
    user_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"USSD Session {self.session_id} - {self.phone_number}"


class USSDMenu(models.Model):
    """Model for USSD menu items"""
    step = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    title_swahili = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    description_swahili = models.TextField(blank=True)
    options = models.JSONField(default=list)
    options_swahili = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['step']
    
    def __str__(self):
        return f"{self.step}: {self.title_swahili}"

