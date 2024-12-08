from celery import shared_task
from pyexpat.errors import messages

from chat.models import Message


@shared_task
def save_message(msg):
    Message.objects.create(
        message=msg.get('msg'),
        chat_id=msg.get('chat_id'),
        user_id=msg.get('user_id')
    )

