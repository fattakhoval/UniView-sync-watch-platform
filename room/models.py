import uuid

from django.db import models
from django.conf import settings
from video.models import Video
from chat.models import Chat

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

