from django.urls import path

from chatPage import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:chatID>/', consumers.ChatConsumer.as_asgi()),
]
