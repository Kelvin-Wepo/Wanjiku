from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatSessionViewSet, SwahiliIntentViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register(r'sessions', ChatSessionViewSet, basename='sessions')
router.register(r'intents', SwahiliIntentViewSet, basename='intents')
router.register(r'messages', ChatMessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
