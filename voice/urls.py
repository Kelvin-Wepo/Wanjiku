from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VoiceSessionViewSet, VoiceRecordingViewSet, VoiceResponseViewSet

router = DefaultRouter()
router.register(r'sessions', VoiceSessionViewSet, basename='sessions')
router.register(r'recordings', VoiceRecordingViewSet, basename='recordings')
router.register(r'responses', VoiceResponseViewSet, basename='responses')

urlpatterns = [
    path('', include(router.urls)),
]
