import africastalking
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import SMSMessage, USSDSession, USSDMenu
from chat.services import SwahiliLLMService
import json


class SMSService:
    """Service for SMS operations"""
    
    def __init__(self):
        africastalking.initialize(
            username=settings.AFRICASTALKING_USERNAME,
            api_key=settings.AFRICASTALKING_API_KEY
        )
        self.sms = africastalking.SMS
        self.llm_service = SwahiliLLMService()
    
    def send_sms(self, phone_number, message, user=None, session_id=None):
        """Send SMS message"""
        try:
            # Send SMS via Africa's Talking
            response = self.sms.send(message, [phone_number])
            
            # Save to database
            sms_message = SMSMessage.objects.create(
                phone_number=phone_number,
                message_type='outgoing',
                content=message,
                content_swahili=message,
                status='sent',
                user=user,
                session_id=session_id
            )
            
            return {
                'success': True,
                'message_id': sms_message.id,
                'response': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_incoming_sms(self, phone_number, message):
        """Process incoming SMS and generate response"""
        try:
            # Save incoming SMS
            SMSMessage.objects.create(
                phone_number=phone_number,
                message_type='incoming',
                content=message,
                content_swahili=message,
                status='delivered'
            )
            
            # Generate response using Swahili LLM
            session_id = f"sms_{phone_number}_{int(timezone.now().timestamp())}"
            response = self.llm_service.process_swahili_message(message, session_id)
            
            # Send response SMS
            sms_result = self.send_sms(phone_number, response, session_id=session_id)
            
            return {
                'success': True,
                'response': response,
                'sms_result': sms_result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


class USSDService:
    """Service for USSD operations"""
    
    def __init__(self):
        self.llm_service = SwahiliLLMService()
    
    def process_ussd_request(self, session_id, phone_number, text):
        """Process USSD request"""
        try:
            # Get or create session
            session, created = USSDSession.objects.get_or_create(
                session_id=session_id,
                defaults={
                    'phone_number': phone_number,
                    'current_step': 'welcome',
                    'expires_at': timezone.now() + timedelta(minutes=5)
                }
            )
            
            if not created:
                session.updated_at = timezone.now()
                session.expires_at = timezone.now() + timedelta(minutes=5)
                session.save()
            
            # Process based on current step
            if text == '' or text == '0':
                return self._show_welcome_menu(session)
            elif text == '1':
                return self._show_services_menu(session)
            elif text == '2':
                return self._show_documents_menu(session)
            elif text == '3':
                return self._show_help_menu(session)
            elif text.startswith('1.'):
                return self._handle_service_request(session, text)
            elif text.startswith('2.'):
                return self._handle_document_request(session, text)
            else:
                return self._handle_text_input(session, text)
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': 'Samahani, kuna tatizo. Tafadhali jaribu tena.'
            }
    
    def _show_welcome_menu(self, session):
        """Show welcome menu"""
        session.current_step = 'welcome'
        session.save()
        
        response = """Karibu Wanjiku 2.0!
Msaidizi wa Serikali wa Kenya

Chagua:
1. Huduma za Serikali
2. Hati za Kidijitali
3. Msaada

0. Ondoka"""
        
        return {
            'success': True,
            'response': response,
            'session_id': session.session_id
        }
    
    def _show_services_menu(self, session):
        """Show services menu"""
        session.current_step = 'services'
        session.save()
        
        response = """Huduma za Serikali:

1.1 Cheti cha Kuzaliwa
1.2 Kitambulisho cha Taifa
1.3 Leseni ya Biashara
1.4 Leseni ya Kuendesha
1.5 Pasipoti

0. Rudi"""
        
        return {
            'success': True,
            'response': response,
            'session_id': session.session_id
        }
    
    def _show_documents_menu(self, session):
        """Show documents menu"""
        session.current_step = 'documents'
        session.save()
        
        response = """Hati za Kidijitali:

2.1 Thibitisha Hati
2.2 Pakia Hati
2.3 Angalia Hati
2.4 Historia ya Hati

0. Rudi"""
        
        return {
            'success': True,
            'response': response,
            'session_id': session.session_id
        }
    
    def _show_help_menu(self, session):
        """Show help menu"""
        session.current_step = 'help'
        session.save()
        
        response = """Msaada:

Wanjiku 2.0 ni msaidizi wako wa serikali.
Anaweza kukusaidia na:
- Huduma za serikali
- Hati za kidijitali
- Maelezo ya mchakato

Andika swali lako au chagua huduma.

0. Rudi"""
        
        return {
            'success': True,
            'response': response,
            'session_id': session.session_id
        }
    
    def _handle_service_request(self, session, text):
        """Handle service request"""
        service_map = {
            '1.1': 'Cheti cha Kuzaliwa',
            '1.2': 'Kitambulisho cha Taifa',
            '1.3': 'Leseni ya Biashara',
            '1.4': 'Leseni ya Kuendesha',
            '1.5': 'Pasipoti'
        }
        
        service_name = service_map.get(text, 'Huduma')
        
        response = f"""Huduma: {service_name}

Maelezo:
- Gharama: Tazama huduma
- Muda: Siku 7-30
- Mahitaji: Cheti cha kuzaliwa, Picha

Kwa maelezo zaidi, andika swali lako.

0. Rudi"""
        
        return {
            'success': True,
            'response': response,
            'session_id': session.session_id
        }
    
    def _handle_document_request(self, session, text):
        """Handle document request"""
        response = """Hati za Kidijitali:

Kwa kutumia blockchain, hati zako zinaaminishwa.
Unaweza:
- Kupakia hati mpya
- Kuthibitisha hati
- Kuangalia historia

Andika 'pakia' au 'thibitisha'

0. Rudi"""
        
        return {
            'success': True,
            'response': response,
            'session_id': session.session_id
        }
    
    def _handle_text_input(self, session, text):
        """Handle free text input"""
        try:
            # Use Swahili LLM to process the text
            response = self.llm_service.process_swahili_message(text, session.session_id)
            
            # Limit response length for USSD
            if len(response) > 160:
                response = response[:157] + "..."
            
            return {
                'success': True,
                'response': response,
                'session_id': session.session_id
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': 'Samahani, kuna tatizo. Tafadhali jaribu tena.'
            }
    
    def end_session(self, session_id):
        """End USSD session"""
        try:
            session = USSDSession.objects.get(session_id=session_id)
            session.status = 'completed'
            session.save()
            
            return {
                'success': True,
                'message': 'Session ended'
            }
            
        except USSDSession.DoesNotExist:
            return {
                'success': False,
                'error': 'Session not found'
            }

