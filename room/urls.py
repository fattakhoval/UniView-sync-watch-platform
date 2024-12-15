from django.urls import path
from room.views import MainPage, CreatedRoom
urlpatterns = [
    path('', MainPage.as_view()),
    path('custom_room/<uuid:room_id>', CreatedRoom.as_view(), name='custom_room'),
]