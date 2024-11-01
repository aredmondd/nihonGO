import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs'].get('username')
        self.room_name = self.scope['url_route']['kwargs'].get('room_name')
        
        if self.username:
            self.room_group_name = f'chat_{self.username}'
        elif self.room_name:
            self.room_group_name = f'chat_{self.room_name}'
        else:
            # handle the case where neither username nor room_name is provided
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender = self.scope["user"].username
        username = data.get("username")
        time = data.get("time")

        if self.username:
            # Broadcast message to user-based room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender
                }
            )
        elif self.room_name:
            # Send message to room-based room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_message",
                    "message": message,
                    "username": username,
                    "time": time
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        time = event["time"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "time": time
        }))
