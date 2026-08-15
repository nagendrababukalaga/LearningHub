from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('', views.ai_assistant_page, name='chat'),
    path('api/query/', views.ai_chat_api, name='api_query'),
]
