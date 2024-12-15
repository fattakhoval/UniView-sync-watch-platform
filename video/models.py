import uuid

from django.db import models


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    url = models.TextField()
    home_url = models.CharField(max_length=200)
    is_our = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
