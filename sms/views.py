from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from .models import SMSMessage, USSDSession, USSDMenu
from .services import SMSService, USSDService
from .serializers import SMSMessageSerializer, USSDSessionSerializer, USSDMenuSerializer


class SMSMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for SMS messages"""
    queryset = SMSMessage.objects.all()
    serializer_class = SMSMessageSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def send_sms(self, request):
        """Send SMS message"""
        phone_number = request.data.get('phone_number')
        message = request.data.get('message')
        
        if not phone_number or not message:
            return Response(
                {'error': 'Phone number and message are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sms_service = SMSService()
        result = sms_service.send_sms(phone_number, message)
        
        if result['success']:
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def process_incoming(self, request):
        """Process incoming SMS"""
        phone_number = request.data.get('phone_number')
        message = request.data.get('message')
        
        if not phone_number or not message:
            return Response(
                {'error': 'Phone number and message are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sms_service = SMSService()
        result = sms_service.process_incoming_sms(phone_number, message)
        
        return Response(result)


class USSDSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for USSD sessions"""
    queryset = USSDSession.objects.all()
    serializer_class = USSDSessionSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def process_request(self, request):
        """Process USSD request"""
        session_id = request.data.get('sessionId')
        phone_number = request.data.get('phoneNumber')
        text = request.data.get('text', '')
        
        if not session_id or not phone_number:
            return Response(
                {'error': 'Session ID and phone number are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ussd_service = USSDService()
        result = ussd_service.process_ussd_request(session_id, phone_number, text)
        
        return Response(result)
    
    @action(detail=False, methods=['post'])
    def end_session(self, request):
        """End USSD session"""
        session_id = request.data.get('sessionId')
        
        if not session_id:
            return Response(
                {'error': 'Session ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ussd_service = USSDService()
        result = ussd_service.end_session(session_id)
        
        return Response(result)


class USSDMenuViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for USSD menus"""
    queryset = USSDMenu.objects.filter(is_active=True)
    serializer_class = USSDMenuSerializer
    permission_classes = [AllowAny]


class SMSWebhookView(APIView):
    """Webhook for incoming SMS from Africa's Talking"""
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        """Handle incoming SMS webhook"""
        try:
            data = request.POST
            phone_number = data.get('from')
            message = data.get('text')
            
            if not phone_number or not message:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing phone number or message'
                }, status=400)
            
            sms_service = SMSService()
            result = sms_service.process_incoming_sms(phone_number, message)
            
            return JsonResponse({
                'status': 'success',
                'message': 'SMS processed',
                'data': result
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)


class USSDWebhookView(APIView):
    """Webhook for USSD requests from Africa's Talking"""
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        """Handle USSD webhook"""
        try:
            data = request.POST
            session_id = data.get('sessionId')
            phone_number = data.get('phoneNumber')
            text = data.get('text', '')
            
            if not session_id or not phone_number:
                return JsonResponse({
                    'response': 'Samahani, kuna tatizo. Tafadhali jaribu tena.',
                    'sessionId': session_id or ''
                })
            
            ussd_service = USSDService()
            result = ussd_service.process_ussd_request(session_id, phone_number, text)
            
            return JsonResponse({
                'response': result.get('response', 'Samahani, kuna tatizo.'),
                'sessionId': result.get('session_id', session_id)
            })
            
        except Exception as e:
            return JsonResponse({
                'response': 'Samahani, kuna tatizo. Tafadhali jaribu tena.',
                'sessionId': request.POST.get('sessionId', '')
            })
