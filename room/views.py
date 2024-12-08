
from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from room.models import Room
from chat.models import Chat


def index(request):
    if request.user.is_authenticated:
        user_id = request.user
    else:
        user_id = AnonymousUser()
    if request.method == 'GET':
        return render(request, template_name='room/room_index.html', context={'user_id': user_id})
    elif request.method == 'POST':
        return create_room(user_id)


def custom_room(request, room_id):
    return render(request, template_name='room/custom_room.html', context={'room_id': room_id, 'room_name': 'hehe'})

def create_room(user_id):

    new_chat = Chat.objects.create()
    new_room = Room.objects.create(
        user_id=user_id,
        chat_id=new_chat
    )
    return redirect(reverse('custom_room', kwargs={'room_id': new_room.id}))
