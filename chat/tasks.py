from celery import shared_task
from django.apps import apps
from django.contrib.auth import get_user_model


@shared_task
def save_message(msg, chat_id, user_id):
    print('hiiii im task')
    Message = apps.get_model('chat', 'Message')
    Chat = apps.get_model('chat', 'Chat')
    User = get_user_model()

    Message.objects.create(
        message=msg,
        chat_id=Chat.objects.get(id=chat_id),
        user_id=User.objects.get(id=user_id)
    )
