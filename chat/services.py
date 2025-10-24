import openai
import json
from django.conf import settings
from .models import SwahiliIntent, ChatSession, ChatMessage
from services.models import GovernmentService


class SwahiliLLMService:
    """Service for handling Swahili language processing"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def process_swahili_message(self, message, session_id):
        """Process a Swahili message and return appropriate response"""
        try:
            # Get or create session
            session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={'language': 'sw'}
            )
            
            # Save user message
            ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=message,
                content_swahili=message
            )
            
            # Detect intent
            intent = self._detect_intent(message)
            
            # Generate response
            response = self._generate_response(message, intent, session)
            
            # Save assistant response
            ChatMessage.objects.create(
                session=session,
                message_type='assistant',
                content=response,
                content_swahili=response,
                is_processed=True
            )
            
            return response
            
        except Exception as e:
            return f"Samahani, kuna tatizo. Tafadhali jaribu tena. (Sorry, there's an issue. Please try again.)"
    
    def _detect_intent(self, message):
        """Detect user intent from Swahili message"""
        # Get all active intents
        intents = SwahiliIntent.objects.filter(is_active=True)
        
        message_lower = message.lower()
        
        # Simple keyword matching for now
        for intent in intents:
            for keyword in intent.keywords:
                if keyword.lower() in message_lower:
                    return intent
        
        # Default intent for general queries
        return None
    
    def _generate_response(self, message, intent, session):
        """Generate appropriate response based on intent"""
        if intent:
            # Use intent-specific response
            response = intent.response_template_swahili
            
            # If it's a service-related intent, add service information
            if intent.service_category:
                services = GovernmentService.objects.filter(
                    category=intent.service_category,
                    is_active=True
                )[:3]
                
                if services:
                    response += "\n\nHuduma zinazopatikana:\n"
                    for service in services:
                        response += f"• {service.name_swahili}\n"
        
        else:
            # Use OpenAI for general conversation
            try:
                prompt = f"""
                Wewe ni Wanjiku, msaidizi wa serikali wa Kenya. Jibu kwa Kiswahili kwa ufupi na kwa urahisi.
                Swali: {message}
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Wanjiku, a helpful Kenyan government assistant. Respond in Swahili."},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                return "Samahani, sikuweza kukusaidia kwa sasa. Tafadhali jaribu tena baadaye."
        
        return response
    
    def get_conversation_history(self, session_id, limit=10):
        """Get conversation history for a session"""
        try:
            session = ChatSession.objects.get(session_id=session_id)
            messages = ChatMessage.objects.filter(session=session).order_by('-timestamp')[:limit]
            return list(reversed(messages))
        except ChatSession.DoesNotExist:
            return []


class SwahiliNLPService:
    """Service for Swahili natural language processing"""
    
    @staticmethod
    def extract_entities(text):
        """Extract entities from Swahili text"""
        entities = {
            'services': [],
            'locations': [],
            'dates': [],
            'numbers': []
        }
        
        # Simple entity extraction (can be enhanced with NER models)
        service_keywords = {
            'cheti cha kuzaliwa': 'birth_certificate',
            'leseni ya biashara': 'business_license',
            'kitambulisho': 'id_card',
            'leseni ya kuendesha': 'driving_license',
            'pasipoti': 'passport'
        }
        
        for keyword, service in service_keywords.items():
            if keyword in text.lower():
                entities['services'].append(service)
        
        return entities
    
    @staticmethod
    def translate_to_english(swahili_text):
        """Translate Swahili text to English for processing"""
        # This would integrate with a translation service
        # For now, return the original text
        return swahili_text
    
    @staticmethod
    def translate_to_swahili(english_text):
        """Translate English text to Swahili"""
        # This would integrate with a translation service
        # For now, return the original text
        return english_text

