from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentVerificationViewSet, BlockchainTransactionViewSet, DocumentTemplateViewSet

router = DefaultRouter()
router.register(r'verifications', DocumentVerificationViewSet, basename='verifications')
router.register(r'transactions', BlockchainTransactionViewSet, basename='transactions')
router.register(r'templates', DocumentTemplateViewSet, basename='templates')

urlpatterns = [
    path('', include(router.urls)),
]
