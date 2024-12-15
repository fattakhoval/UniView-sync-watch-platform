from django.urls import path
from chat.views import get_message_by_chat_id


urlpatterns = [
    path('get/', get_message_by_chat_id),
]