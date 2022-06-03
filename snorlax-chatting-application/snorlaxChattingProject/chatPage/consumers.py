import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from .views import get_current_chat, get_last_10_messages, get_author

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        # gets the last 10 messages of the chat from the database

        messages = get_last_10_messages(data['chatID'])
        content = {
            "command": "messages",
            "messages": self.messages_to_json(messages),
        }
        self.send_message(content)

    def new_message(self, data):
        # creates a new message and saves it to the database
        # then sends the message to the chat room

        author = get_author(data["from"])

        content_message = data["message"]
        message = Message.objects.create(
            author=author,
            content=content_message,
            chat=get_current_chat(data["chatID"])
        )
        message.save()

        content = {
            "command": "new_message",
            "message": self.message_to_json(message)
        }
        self.send_chat_message(content)

    def messages_to_json(self, messages):
        # converts the messages to json
        res = []
        if messages:
            for message in messages:
                res.append(self.message_to_json(message))
            return res

    def message_to_json(self, message):
        # converts the message to json
        return {
            "id": message.id,
            "author": message.author.username,
            "content": message.content,
            "timestamp": str(message.timestamp)
        }

    # the commands to dictate which function to run
    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message
    }

    def connect(self):
        # connects to the chat room
        self.room_name = self.scope["url_route"]["kwargs"]["chatID"]

        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # disconnects from the chat room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # receives the data and then calls the appropriate function
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        # sends the message to the chat room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        # Send message to websocket
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        # Send message to websocket
        self.send(text_data=json.dumps(message))
