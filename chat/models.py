from django.db import models
from django.contrib.auth.models import User


class ChatSession(models.Model):
    """Model for chat sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=10, default='sw')  # 'sw' for Swahili, 'en' for English
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session {self.session_id}"


class ChatMessage(models.Model):
    """Model for chat messages"""
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    content_swahili = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}"


class SwahiliIntent(models.Model):
    """Model for Swahili intents and responses"""
    intent_name = models.CharField(max_length=100)
    intent_name_swahili = models.CharField(max_length=100)
    keywords = models.JSONField(default=list)  # Keywords in Swahili
    response_template = models.TextField()
    response_template_swahili = models.TextField()
    service_category = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['intent_name']
    
    def __str__(self):
        return self.intent_name_swahili

