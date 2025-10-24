from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import GovernmentService, ServiceRequest, ServiceFAQ
from .serializers import GovernmentServiceSerializer, ServiceRequestSerializer, ServiceFAQSerializer


class GovernmentServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for government services"""
    queryset = GovernmentService.objects.filter(is_active=True)
    serializer_class = GovernmentServiceSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search services by name or description"""
        query = request.query_params.get('q', '')
        if query:
            queryset = self.queryset.filter(
                Q(name__icontains=query) |
                Q(name_swahili__icontains=query) |
                Q(description__icontains=query) |
                Q(description_swahili__icontains=query)
            )
        else:
            queryset = self.queryset
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get services by category"""
        category = request.query_params.get('category', '')
        if category:
            queryset = self.queryset.filter(category=category)
        else:
            queryset = self.queryset
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ServiceRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for service requests"""
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ServiceRequest.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update service request status"""
        service_request = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in [choice[0] for choice in ServiceRequest.STATUS_CHOICES]:
            service_request.status = new_status
            service_request.save()
            return Response({'status': 'updated'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class ServiceFAQViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for service FAQs"""
    queryset = ServiceFAQ.objects.filter(is_active=True)
    serializer_class = ServiceFAQSerializer
    
    def get_queryset(self):
        service_id = self.request.query_params.get('service_id')
        if service_id:
            return self.queryset.filter(service_id=service_id)
        return self.queryset

