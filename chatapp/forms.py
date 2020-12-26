from django.forms import ModelForm, DateInput
from datetime import datetime, date
from .models import *
from django import forms
import datetime


class ChatroomCreationForm(ModelForm):

    class Meta:
        model = Chatroom
        fields = [
            'title',
            'description',
            'is_anonymous_supported',
            'is_private',
            'password',
        ]

    password = forms.CharField(widget=forms.PasswordInput)


class ChatForm(ModelForm):

    class Meta:
        model = Chats
        fields = [
            'chat_body',
        ]