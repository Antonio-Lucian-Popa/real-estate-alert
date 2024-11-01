"""
ASGI config for real_estate_alert project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import listings.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_alert.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Configurare pentru WebSocket, unde vei adăuga mai târziu rutele tale WebSocket
    "websocket": AuthMiddlewareStack(
        URLRouter(
            listings.routing.websocket_urlpatterns
        )
    ),
})
