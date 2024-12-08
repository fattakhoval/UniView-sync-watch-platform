from django.contrib import admin
from room.models import Room

@admin.register(Room)
class ChatAdmin(admin.ModelAdmin):
    pass

