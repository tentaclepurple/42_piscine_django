# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    # dictionary to store connected users for each room
    connected_users = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        # initialize connected users list for the room
        if self.room_group_name not in ChatConsumer.connected_users:
            ChatConsumer.connected_users[self.room_group_name] = set()

        # add user to the room's connected users list
        ChatConsumer.connected_users[self.room_group_name].add(self.user.username)

        # join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # send the list of connected users to the client
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': list(ChatConsumer.connected_users[self.room_group_name])
            }
        )

        # notify that the user has joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'username': self.user.username
            }
        )

    async def disconnect(self, close_code):
        if not self.user.is_authenticated:
            return

        # remove user from the room's connected users list
        if self.room_group_name in ChatConsumer.connected_users:
            ChatConsumer.connected_users[self.room_group_name].discard(self.user.username)
            
            # notify that the user has left
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_left',
                    'username': self.user.username
                }
            )

            # update the list of connected users
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_list',
                    'users': list(ChatConsumer.connected_users[self.room_group_name])
                }
            )

        # leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        if not self.user.is_authenticated:
            return
            
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # save the message to the database
        await self.save_message(message)

        # send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username']
        }))

    async def user_list(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))

    async def user_joined(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'username': event['username']
        }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'username': event['username']
        }))

    @database_sync_to_async
    def save_message(self, message):
        room = ChatRoom.objects.get(name=self.room_name)
        Message.objects.create(
            room=room,
            user=self.user,
            content=message
        )
