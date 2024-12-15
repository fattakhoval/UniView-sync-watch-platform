from django.contrib import admin
from chat.models import Chat, Message



class MessageInline(admin.TabularInline):
    model = Message
    extra = 0  # Количество пустых форм для добавления новых сообщений
    verbose_name = "Сообщение"
    verbose_name_plural = "Сообщения"
    ordering = ['created_at']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
    list_display = ('id', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ('username', 'message', 'chat_id', 'created_at')
    list_filter = ('chat_id', 'user_id')
    list_per_page = 50

    ordering = ('-created_at',)

    def username(self, obj):
        return obj.user_id.username

