from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()


class Contact(models.Model):
    # contact book a list of user who are friend of the original user
    owner = models.ForeignKey(User, related_name="contact_book", on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name="friends")

    def __str__(self):
        return self.owner.username


class Chat(models.Model):
    # chat consists of multiple users and
    # is connected with messages related to that chat
    # get_last_message- returns the last message in that chat

    participants = models.ManyToManyField(
                    User, blank=True)

    def get_last_message(self):
        return self.chat_messages.order_by('-timestamp').all()[0]

    def __str__(self):
        return "{}".format(self.pk)


class Message(models.Model):
    author = models.ForeignKey(
                    User, related_name="author_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, related_name="chat_messages", on_delete=models.CASCADE)
