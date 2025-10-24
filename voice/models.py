from django.db import models
from django.contrib.auth.models import User


class VoiceSession(models.Model):
    """Model for voice interaction sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=10, default='sw')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Voice Session {self.session_id}"


class VoiceRecording(models.Model):
    """Model for voice recordings"""
    session = models.ForeignKey(VoiceSession, on_delete=models.CASCADE, related_name='recordings')
    audio_file = models.FileField(upload_to='voice_recordings/')
    transcript = models.TextField(blank=True)
    transcript_swahili = models.TextField(blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)  # Duration in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Recording {self.id} - {self.transcript[:50]}"


class VoiceResponse(models.Model):
    """Model for voice responses"""
    session = models.ForeignKey(VoiceSession, on_delete=models.CASCADE, related_name='responses')
    text_response = models.TextField()
    audio_file = models.FileField(upload_to='voice_responses/', null=True, blank=True)
    response_type = models.CharField(max_length=20, default='text')  # 'text' or 'audio'
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Response {self.id} - {self.text_response[:50]}"

