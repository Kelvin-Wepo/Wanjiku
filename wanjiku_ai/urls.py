"""
URL configuration for wanjiku_ai project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/services/', include('services.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/voice/', include('voice.urls')),
    path('api/blockchain/', include('blockchain.urls')),
    path('api/sms/', include('sms.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
