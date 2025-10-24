from django.db import models
from django.contrib.auth.models import User


class GovernmentService(models.Model):
    """Model for government services available through Wanjiku"""
    SERVICE_CATEGORIES = [
        ('identity', 'Identity Documents'),
        ('business', 'Business Services'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('transport', 'Transport'),
        ('agriculture', 'Agriculture'),
        ('social', 'Social Services'),
    ]
    
    name = models.CharField(max_length=200)
    name_swahili = models.CharField(max_length=200)
    description = models.TextField()
    description_swahili = models.TextField()
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES)
    requirements = models.JSONField(default=list)
    requirements_swahili = models.JSONField(default=list)
    processing_time = models.CharField(max_length=100)
    processing_time_swahili = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    """Model for user service requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(GovernmentService, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_data = models.JSONField(default=dict)
    appointment_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.service.name}"


class ServiceFAQ(models.Model):
    """Model for frequently asked questions about services"""
    service = models.ForeignKey(GovernmentService, on_delete=models.CASCADE, related_name='faqs')
    question = models.TextField()
    question_swahili = models.TextField()
    answer = models.TextField()
    answer_swahili = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['question']
    
    def __str__(self):
        return self.question

