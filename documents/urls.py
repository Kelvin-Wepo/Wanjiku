from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentCategoryViewSet, DocumentTemplateViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='documents')
router.register(r'categories', DocumentCategoryViewSet, basename='categories')
router.register(r'templates', DocumentTemplateViewSet, basename='templates')

urlpatterns = [
    path('', include(router.urls)),
]
