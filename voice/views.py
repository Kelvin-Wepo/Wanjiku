from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, FileResponse
from django.utils import timezone
import uuid
from .models import VoiceSession, VoiceRecording, VoiceResponse
from .services import SwahiliVoiceService
from .serializers import VoiceSessionSerializer, VoiceRecordingSerializer, VoiceResponseSerializer


class VoiceSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for voice sessions"""
    queryset = VoiceSession.objects.all()
    serializer_class = VoiceSessionSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def process_voice(self, request):
        """Process voice input"""
        audio_file = request.FILES.get('audio')
        session_id = request.data.get('session_id', str(uuid.uuid4()))
        
        if not audio_file:
            return Response({'error': 'Audio file is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        voice_service = SwahiliVoiceService()
        result = voice_service.process_voice_input(audio_file, session_id)
        
        return Response(result)
    
    @action(detail=False, methods=['post'])
    def generate_response(self, request):
        """Generate voice response from text"""
        text = request.data.get('text', '')
        session_id = request.data.get('session_id', str(uuid.uuid4()))
        
        if not text:
            return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        voice_service = SwahiliVoiceService()
        result = voice_service.generate_voice_response(text, session_id)
        
        return Response(result)
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get voice session history"""
        session = self.get_object()
        voice_service = SwahiliVoiceService()
        history = voice_service.get_session_history(session.session_id)
        
        return Response(history)
    
    @action(detail=False, methods=['post'])
    def create_session(self, request):
        """Create a new voice session"""
        session_id = str(uuid.uuid4())
        language = request.data.get('language', 'sw')
        
        session = VoiceSession.objects.create(
            session_id=session_id,
            language=language
        )
        
        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VoiceRecordingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for voice recordings"""
    queryset = VoiceRecording.objects.all()
    serializer_class = VoiceRecordingSerializer
    permission_classes = [AllowAny]
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download audio file"""
        recording = self.get_object()
        if recording.audio_file:
            return FileResponse(
                recording.audio_file.open(),
                as_attachment=True,
                filename=f'recording_{recording.id}.wav'
            )
        return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)


class VoiceResponseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for voice responses"""
    queryset = VoiceResponse.objects.all()
    serializer_class = VoiceResponseSerializer
    permission_classes = [AllowAny]
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download audio response"""
        response = self.get_object()
        if response.audio_file:
            return FileResponse(
                response.audio_file.open(),
                as_attachment=True,
                filename=f'response_{response.id}.wav'
            )
        return Response({'error': 'Audio file not found'}, status=status.HTTP_404_NOT_FOUND)

