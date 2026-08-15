from django.urls import path
from . import views

app_name = 'memory'

urlpatterns = [
    path('hub/', views.memory_hub, name='memory_hub'),
    path('save/<int:topic_id>/', views.save_memory_ajax, name='save_memory_ajax'),
    path('doubts/', views.doubts_list, name='doubts_list'),
    path('doubts/create/', views.create_doubt, name='create_doubt'),
    path('doubts/<int:doubt_id>/toggle/', views.toggle_doubt_resolve, name='toggle_doubt_resolve'),
    path('mistakes/', views.mistakes_list, name='mistakes_list'),
    path('mistakes/create/', views.create_mistake, name='create_mistake'),
    path('mistakes/<int:mistake_id>/delete/', views.delete_mistake, name='delete_mistake'),
]
