# chat/views.py

from django.shortcuts import render
from .models import ChatRoom, Message


def index(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chat/index.html', {'chatrooms': chatrooms})


def room(request, room_name):
    chatroom = ChatRoom.objects.get(name=room_name)
    last_messages = chatroom.messages.order_by('-timestamp')[:3][::-1]
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chatroom': chatroom,
        'last_messages': last_messages
    })
