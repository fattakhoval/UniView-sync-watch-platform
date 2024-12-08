from django.urls import path
from room.views import index, custom_room

urlpatterns = [
    path('',index),
    path('custom_room/<uuid:room_id>', custom_room, name='custom_room'),
]