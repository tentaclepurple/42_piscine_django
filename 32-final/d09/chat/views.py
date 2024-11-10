# chat/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatRoom


@login_required
def index(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chat/index.html', {'chatrooms': chatrooms})


@login_required
def room(request, room_name):
    chatroom = ChatRoom.objects.get(name=room_name)
    messages = chatroom.messages.all()
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chatroom': chatroom,
        'messages': messages
    })
