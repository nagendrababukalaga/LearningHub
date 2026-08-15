from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('path/', views.path_overview, name='path_overview'),
    path('topics/<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('resources/<int:resource_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.bookmarks_list, name='bookmarks_list'),
]
