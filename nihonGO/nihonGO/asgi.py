import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from ChitChat.consumers import ChatConsumer  # Corrected import

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nihonGO.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # This will handle regular HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # This should match the URL pattern defined in your routing.py
            re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
        ])
    ),
})
