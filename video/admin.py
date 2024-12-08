from django.contrib import admin

from video.models import Video


@admin.register(Video)
class ChatAdmin(admin.ModelAdmin):
    pass

