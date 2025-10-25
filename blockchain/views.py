from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from .models import DocumentVerification, BlockchainTransaction, DocumentTemplate
from .services import DocumentVerificationService
from .serializers import DocumentVerificationSerializer, BlockchainTransactionSerializer, DocumentTemplateSerializer


class DocumentVerificationViewSet(viewsets.ModelViewSet):
    """ViewSet for document verification"""
    serializer_class = DocumentVerificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DocumentVerification.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def upload_document(self, request):
        """Upload a document for verification"""
        document_file = request.FILES.get('document')
        document_type = request.data.get('document_type')
        verification_data = request.data.get('verification_data', {})
        
        if not document_file or not document_type:
            return Response(
                {'error': 'Document file and type are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        verification_service = DocumentVerificationService()
        result = verification_service.upload_document(
            request.user,
            document_file,
            document_type,
            verification_data
        )
        
        if result['success']:
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify_document(self, request):
        """Verify a document using blockchain"""
        document_hash = request.data.get('document_hash')
        
        if not document_hash:
            return Response(
                {'error': 'Document hash is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        verification_service = DocumentVerificationService()
        result = verification_service.verify_document(document_hash)
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def check_status(self, request):
        """Check document verification status"""
        document_hash = request.query_params.get('document_hash')
        
        if not document_hash:
            return Response(
                {'error': 'Document hash is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        verification_service = DocumentVerificationService()
        result = verification_service.get_document_status(document_hash)
        
        return Response(result)
    
    @action(detail=True, methods=['get'])
    def download_document(self, request, pk=None):
        """Download original document"""
        verification = self.get_object()
        if verification.original_file:
            return FileResponse(
                verification.original_file.open(),
                as_attachment=True,
                filename=f'{verification.document_type}_{verification.id}.pdf'
            )
        return Response({'error': 'Document file not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def validate_document(self, request):
        """Validate document format"""
        document_file = request.FILES.get('document')
        document_type = request.data.get('document_type')
        
        if not document_file or not document_type:
            return Response(
                {'error': 'Document file and type are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        verification_service = DocumentVerificationService()
        result = verification_service.validate_document(document_file, document_type)
        
        return Response(result)

    @action(detail=False, methods=['post'])
    def notarize_document(self, request):
        """Notarize an existing uploaded document on-chain"""
        document_id = request.data.get('document_id')
        if not document_id:
            return Response({'error': 'document_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            verification = DocumentVerification.objects.get(id=document_id, user=request.user)
        except DocumentVerification.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

        # Call Ethereum service to store the document hash on-chain
        from .services import EthereumService
        eth_service = EthereumService()
        result = eth_service.store_document_hash(verification.document_hash, {
            'user_id': request.user.id,
            'document_type': verification.document_type,
            'ipfs_cid': getattr(verification, 'ipfs_cid', '')
        })

        if not result.get('success'):
            return Response({'success': False, 'error': result.get('error')}, status=status.HTTP_400_BAD_REQUEST)

        # create blockchain transaction record
        BlockchainTransaction.objects.create(
            document_verification=verification,
            tx_hash=result.get('tx_hash'),
            block_number=result.get('block_number'),
            status='confirmed'
        )

        verification.blockchain_tx_hash = result.get('tx_hash')
        verification.save()

        return Response({'success': True, 'tx_hash': result.get('tx_hash')})


class BlockchainTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for blockchain transactions"""
    queryset = BlockchainTransaction.objects.all()
    serializer_class = BlockchainTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BlockchainTransaction.objects.filter(
            document_verification__user=self.request.user
        )


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

