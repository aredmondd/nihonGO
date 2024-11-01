"""
ASGI config for nihonGO project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
import nihonGO.theme.routing as nihonGO_routing  # Adjust according to actual app structure
import nihonGO.theme.routing as ChitChat_routing

# Set the default settings module for the 'nihonGO' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nihonGO.settings')
nihonGO_application = get_asgi_application()

# Set the default settings module for the 'DjangoChat' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoChat.settings')
DjangoChat_application = get_asgi_application()

# Create the ASGI application dispatcher
application = ProtocolTypeRouter({
    "http": URLRouter([
        path('nihongo/', nihonGO_application),
        path('djangochat/', DjangoChat_application),
    ]),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            nihonGO_routing.websocket_urlpatterns +
            ChitChat_routing.websocket_urlpatterns
        )
    ),
})
