from django.urls import path

from receiver.consumer import Consumer

websocket_urlpatterns = [
    path('ws/arduino/', Consumer.as_asgi()),
]