"""
ASGI config for arduino_controll_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

import receiver.routing as receiver


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arduino_controll_server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        receiver.websocket_urlpatterns
    )
})
