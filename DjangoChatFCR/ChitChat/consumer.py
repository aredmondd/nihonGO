import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

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
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        time = text_data_json["time"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_message",
                "message": message,
                "username": username,
                "time": time
            }
        )

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
