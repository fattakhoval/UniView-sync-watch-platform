from django.http import JsonResponse
from chat.models import Message

def get_message_by_chat_id(request):
    chat_id = request.GET.get('chat_id')

    messages = Message.objects.filter(chat_id=chat_id)

    return JsonResponse({'messages': list(messages)})
