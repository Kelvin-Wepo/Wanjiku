import speech_recognition as sr
import pyttsx3
import tempfile
import os
from django.conf import settings
from django.core.files.base import ContentFile
from .models import VoiceSession, VoiceRecording, VoiceResponse
import uuid


class SwahiliVoiceService:
    """Service for Swahili voice recognition and synthesis"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self._setup_tts()
    
    def _setup_tts(self):
        """Setup text-to-speech engine for Swahili"""
        voices = self.tts_engine.getProperty('voices')
        # Try to find a Swahili-compatible voice
        for voice in voices:
            if 'sw' in voice.id.lower() or 'kenya' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Set speech rate and volume
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.8)  # Volume level
    
    def transcribe_audio(self, audio_file_path, language='sw-KE'):
        """Transcribe audio file to text"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            # Use Google Speech Recognition with Swahili language
            text = self.recognizer.recognize_google(audio, language=language)
            return text, 0.8  # Return text and confidence score
            
        except sr.UnknownValueError:
            return "Samahani, sikuweza kusikia vizuri. Tafadhali sema tena.", 0.0
        except sr.RequestError as e:
            return f"Tatizo la huduma: {str(e)}", 0.0
        except Exception as e:
            return f"Kosa: {str(e)}", 0.0
    
    def text_to_speech(self, text, language='sw'):
        """Convert text to speech"""
        try:
            # Create temporary file for audio output
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_path = temp_file.name
            
            # Save audio to temporary file
            self.tts_engine.save_to_file(text, temp_path)
            self.tts_engine.runAndWait()
            
            # Read the generated audio file
            with open(temp_path, 'rb') as f:
                audio_content = f.read()
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return audio_content
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return None
    
    def process_voice_input(self, audio_file, session_id):
        """Process voice input and return response"""
        try:
            # Get or create voice session
            session, created = VoiceSession.objects.get_or_create(
                session_id=session_id,
                defaults={'language': 'sw'}
            )
            
            # Save audio file temporarily for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name
            
            # Transcribe audio
            transcript, confidence = self.transcribe_audio(temp_path)
            
            # Save recording to database
            recording = VoiceRecording.objects.create(
                session=session,
                audio_file=audio_file,
                transcript=transcript,
                transcript_swahili=transcript,
                confidence_score=confidence
            )
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return {
                'transcript': transcript,
                'confidence': confidence,
                'recording_id': recording.id
            }
            
        except Exception as e:
            return {
                'error': f"Tatizo la kusindikiza sauti: {str(e)}",
                'transcript': '',
                'confidence': 0.0
            }
    
    def generate_voice_response(self, text, session_id):
        """Generate voice response from text"""
        try:
            session = VoiceSession.objects.get(session_id=session_id)
            
            # Generate audio from text
            audio_content = self.text_to_speech(text)
            
            if audio_content:
                # Save response to database
                response = VoiceResponse.objects.create(
                    session=session,
                    text_response=text,
                    response_type='audio'
                )
                
                # Save audio file
                audio_file = ContentFile(audio_content, name=f'response_{response.id}.wav')
                response.audio_file.save(f'response_{response.id}.wav', audio_file)
                
                return {
                    'audio_url': response.audio_file.url,
                    'text': text,
                    'response_id': response.id
                }
            else:
                # Fallback to text response
                response = VoiceResponse.objects.create(
                    session=session,
                    text_response=text,
                    response_type='text'
                )
                
                return {
                    'text': text,
                    'response_id': response.id
                }
                
        except Exception as e:
            return {
                'error': f"Tatizo la kutoa jibu: {str(e)}",
                'text': text
            }
    
    def get_session_history(self, session_id):
        """Get voice session history"""
        try:
            session = VoiceSession.objects.get(session_id=session_id)
            recordings = VoiceRecording.objects.filter(session=session).order_by('created_at')
            responses = VoiceResponse.objects.filter(session=session).order_by('created_at')
            
            return {
                'recordings': [
                    {
                        'id': r.id,
                        'transcript': r.transcript_swahili,
                        'confidence': r.confidence_score,
                        'timestamp': r.created_at.isoformat()
                    } for r in recordings
                ],
                'responses': [
                    {
                        'id': r.id,
                        'text': r.text_response,
                        'type': r.response_type,
                        'audio_url': r.audio_file.url if r.audio_file else None,
                        'timestamp': r.created_at.isoformat()
                    } for r in responses
                ]
            }
        except VoiceSession.DoesNotExist:
            return {'error': 'Session not found'}

