from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SMSMessageViewSet, USSDSessionViewSet, USSDMenuViewSet, SMSWebhookView, USSDWebhookView

router = DefaultRouter()
router.register(r'sms', SMSMessageViewSet, basename='sms')
router.register(r'ussd/sessions', USSDSessionViewSet, basename='ussd-sessions')
router.register(r'ussd/menus', USSDMenuViewSet, basename='ussd-menus')

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/sms/', SMSWebhookView.as_view(), name='sms_webhook'),
    path('webhooks/ussd/', USSDWebhookView.as_view(), name='ussd_webhook'),
]
