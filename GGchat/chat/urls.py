from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_rooms, name='chat_rooms'),
    path('create/', views.create_room, name='create_room'),
    path('<slug:room_slug>/', views.chat_room, name='chat_room'),
]