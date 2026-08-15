from django.urls import path
from . import views

app_name = 'bootcamp'

urlpatterns = [
    path('', views.bootcamp_index, name='index'),
    path('day/<int:day_number>/', views.bootcamp_day_detail, name='day_detail'),
    path('day/<int:day_number>/toggle/', views.toggle_day_complete, name='toggle_day_complete'),
]
