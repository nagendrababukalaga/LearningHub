"""
URL configuration for LearningHub project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('learning/', include('apps.learning.urls', namespace='learning')),
    path('memory/', include('apps.memory.urls', namespace='memory')),
    path('progress/', include('apps.progress.urls', namespace='progress')),
    path('bootcamp/', include('apps.bootcamp.urls', namespace='bootcamp')),
    path('guidance/', include('apps.guidance.urls', namespace='guidance')),
    path('ai-assistant/', include('apps.ai_assistant.urls', namespace='ai_assistant')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'
