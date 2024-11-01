from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/user/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),  # For user-based chat
    re_path(r'ws/chat/room/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),  # For room-based chat
]
