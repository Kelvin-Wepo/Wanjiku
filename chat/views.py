from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
import uuid
from .models import ChatSession, ChatMessage, SwahiliIntent
from .services import SwahiliLLMService, SwahiliNLPService
from .serializers import ChatSessionSerializer, ChatMessageSerializer, SwahiliIntentSerializer


class ChatSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for chat sessions"""
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """Send a message to Wanjiku"""
        message = request.data.get('message', '')
        session_id = request.data.get('session_id', str(uuid.uuid4()))
        language = request.data.get('language', 'sw')
        
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Process message with Swahili LLM
        llm_service = SwahiliLLMService()
        response = llm_service.process_swahili_message(message, session_id)
        
        return Response({
            'response': response,
            'session_id': session_id,
            'timestamp': timezone.now().isoformat()
        })
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get chat history for a session"""
        session = self.get_object()
        messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
        
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def create_session(self, request):
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        language = request.data.get('language', 'sw')
        
        session = ChatSession.objects.create(
            session_id=session_id,
            language=language
        )
        
        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SwahiliIntentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Swahili intents"""
    queryset = SwahiliIntent.objects.filter(is_active=True)
    serializer_class = SwahiliIntentSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def detect_intent(self, request):
        """Detect intent from Swahili text"""
        text = request.data.get('text', '')
        
        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract entities
        entities = SwahiliNLPService.extract_entities(text)
        
        # Find matching intent
        intents = SwahiliIntent.objects.filter(is_active=True)
        matched_intent = None
        
        for intent in intents:
            for keyword in intent.keywords:
                if keyword.lower() in text.lower():
                    matched_intent = intent
                    break
            if matched_intent:
                break
        
        return Response({
            'intent': SwahiliIntentSerializer(matched_intent).data if matched_intent else None,
            'entities': entities
        })


class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for chat messages"""
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [AllowAny]

