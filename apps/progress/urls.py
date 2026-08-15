from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('update/<int:topic_id>/', views.update_progress_ajax, name='update_progress_ajax'),
    path('practice/', views.practice_list, name='practice_list'),
    path('practice/<int:problem_id>/submit/', views.practice_submit_ajax, name='practice_submit_ajax'),
    path('revision/', views.revision_hub, name='revision_hub'),
]
