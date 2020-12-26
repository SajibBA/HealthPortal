from django.db import models

# Create your models here.

from profiles.models import Person


class Chatroom(models.Model):
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_anonymous_supported = models.BooleanField(default=False)
    is_private = models.BooleanField(default=True)
    password = models.CharField(max_length=50)


class Chats(models.Model):
    sender = models.CharField(max_length=50)
    chat_body = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    chat_room = models.ForeignKey(Chatroom, on_delete=models.CASCADE)

