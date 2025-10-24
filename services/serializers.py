from rest_framework import serializers
from .models import GovernmentService, ServiceRequest, ServiceFAQ


class GovernmentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentService
        fields = '__all__'


class ServiceRequestSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_name_swahili = serializers.CharField(source='service.name_swahili', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class ServiceFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFAQ
        fields = '__all__'

