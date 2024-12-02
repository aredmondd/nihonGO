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
            # Updated regex to allow URL-encoded room names
            re_path(r'ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer.as_asgi()),
        ])
    ),
})
