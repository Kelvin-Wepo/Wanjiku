from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GovernmentServiceViewSet, ServiceRequestViewSet, ServiceFAQViewSet

router = DefaultRouter()
router.register(r'services', GovernmentServiceViewSet, basename='services')
router.register(r'requests', ServiceRequestViewSet, basename='requests')
router.register(r'faqs', ServiceFAQViewSet, basename='faqs')

urlpatterns = [
    path('', include(router.urls)),
]
