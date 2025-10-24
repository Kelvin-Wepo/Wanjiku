from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from .models import Document, DocumentCategory, DocumentTemplate
from .serializers import DocumentSerializer, DocumentCategorySerializer, DocumentTemplateSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for user documents"""
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download document file"""
        document = self.get_object()
        if document.file:
            return FileResponse(
                document.file.open(),
                as_attachment=True,
                filename=f'{document.title}_{document.id}.pdf'
            )
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get documents by type"""
        document_type = request.query_params.get('document_type')
        if document_type:
            queryset = self.get_queryset().filter(document_type=document_type)
        else:
            queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        """Get verified documents"""
        queryset = self.get_queryset().filter(is_verified=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DocumentCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for document categories"""
    queryset = DocumentCategory.objects.filter(is_active=True)
    serializer_class = DocumentCategorySerializer
    permission_classes = [IsAuthenticated]


class DocumentTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for document templates"""
    queryset = DocumentTemplate.objects.filter(is_active=True)
    serializer_class = DocumentTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get templates by document type"""
        document_type = request.query_params.get('document_type')
        if document_type:
            queryset = self.queryset.filter(document_type=document_type)
        else:
            queryset = self.queryset
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

