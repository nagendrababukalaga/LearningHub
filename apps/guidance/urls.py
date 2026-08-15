from django.urls import path
from . import views

app_name = 'guidance'

urlpatterns = [
    path('', views.guidance_home, name='home'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('pro/', views.pricing_concept, name='pricing_concept'),
]
