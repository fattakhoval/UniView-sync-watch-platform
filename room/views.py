from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from core.form import UserRegistrationForm

from room.models import Room
from chat.models import Chat, Message


class MainPage(LoginRequiredMixin, TemplateView):

    template_name = 'room/room_index.html'

    login_url = '/accounts/login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id

        return context

    def post(self, request, *args, **kwargs):
        new_chat = Chat.objects.create()
        new_room = Room.objects.create(
            user_id=request.user,
            chat_id=new_chat
        )
        return HttpResponseRedirect(reverse('custom_room', kwargs={'room_id': new_room.id}))


class CreatedRoom(LoginRequiredMixin, TemplateView):

    template_name = 'room/custom_room.html'

    login_url = '/accounts/login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        room_id = kwargs.get('room_id')
        room = Room.objects.get(id=room_id)

        context['chat_id'] = room.chat_id.id
        context['user_id'] = self.request.user.id

        user = User.objects.get(id=self.request.user.id)

        context['username'] = user.username

        context['messages'] = Message.objects.filter(chat_id=room.chat_id.id).select_related('user_id').values('id', 'message', 'user_id__username', 'created_at')

        return context


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            return redirect('/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'django_registration/registration_form.html', {'form': user_form})