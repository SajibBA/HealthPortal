from django.urls import reverse_lazy
from pyexpat.errors import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.utils.translation import ugettext_lazy as _

# Create your views here.
from chatapp.filters import *
from chatapp.forms import *


def create_chatroom(request):
    form = ChatroomCreationForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        is_anonymous_supported = form.cleaned_data['is_anonymous_supported']
        is_private = form.cleaned_data['is_private']
        password = form.cleaned_data['password']
        Chatroom.objects.get_or_create(
            creator=request.user,
            title=title,
            description=description,
            is_anonymous_supported=is_anonymous_supported,
            is_private=is_private,
            password=password,
        )
        return HttpResponseRedirect(reverse('view_chatroom'))
    return render(request, 'chatroom/create_chatroom.html', {'form': form})


def view_chatroom(request):
    chatroom = Chatroom.objects.all()
    myFilter = ChatroomFilter(request.GET, queryset=chatroom)
    chatroom = myFilter.qs
    context = {'chatroom': chatroom, 'myFilter': myFilter}
    return render(request, 'chatroom/view_chatroom.html', context)


def live_chatroom(request, pk):
    try:
        chat_room = Chatroom.objects.get(pk=pk)
    except Person.DoesNotExist:
        raise Http404
    chat_all = Chats.objects.filter(chat_room=chat_room)
    sender_person = request.user.username
    if request.method =='POST':
        chat_body = request.POST['chat_body']
        sender = request.user
        chat_room = chat_room
        chat = Chats.objects.create(
            chat_body=chat_body,
            sender=sender,
            chat_room=chat_room,
        )
        context = {'chat_room': chat_room, 'chat': chat, 'chat_all': chat_all,
                   'sender_person': sender_person}
        return render(request, 'chatroom/livechatroom.html', context)
    else:
        context = {'chat_room': chat_room, 'chat_all': chat_all,
                   'sender_person': sender_person}
        return render(request, 'chatroom/livechatroom.html', context)


def protected_chatroom(request, pk):
    try:
        chat_room = Chatroom.objects.get(pk=pk)
    except Chatroom.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        password_get = request.POST['password_get']
        if chat_room.password == password_get:
            context = {'chat_room': chat_room}
            if chat_room.is_anonymous_supported:
                return render(request, 'chatroom/join_chatroom.html', context)
            else:
                return render(request, 'chatroom/livechatroom.html', context)
        else:
            context = {'chat_room': chat_room}
            messages.error(request, 'Wrong Password!')
            return render(request, 'chatroom/protected_chatroom.html', context)
    else:
        context = {'chat_room': chat_room}
        return render(request, 'chatroom/protected_chatroom.html', context)


def join_chatroom(request, pk):
    try:
        chat_room = Chatroom.objects.get(pk=pk)
    except Chatroom.DoesNotExist:
        raise Http404
    context = {'chat_room': chat_room}
    return render(request, 'chatroom/join_chatroom.html', context)


def anonymous_chatroom(request, pk):
    try:
        chat_room = Chatroom.objects.get(pk=pk)
    except Person.DoesNotExist:
        raise Http404
    chat_all = Chats.objects.filter(chat_room=chat_room)
    live_person = request.user
    if request.method =='POST':
        chat_body = request.POST['chat_body']
        sender = 'anonymous'
        chat_room = chat_room
        chat = Chats.objects.create(
            chat_body=chat_body,
            sender= sender,
            chat_room=chat_room,
        )
        context = {'chat_room': chat_room, 'chat': chat, 'chat_all': chat_all,
                   'live_person': live_person}
        return render(request, 'chatroom/anonymous_chatroom.html', context)
    else:
        context = {'chat_room': chat_room, 'chat_all': chat_all,
                   'live_person': live_person}
        return render(request, 'chatroom/anonymous_chatroom.html', context)


def mychatrooms(request):
    chatroom = Chatroom.objects.filter(creator=request.user)
    myFilter = ChatroomFilter(request.GET, queryset=chatroom)
    chatroom = myFilter.qs
    context = {'chatroom': chatroom, 'myFilter': myFilter}
    return render(request, 'chatroom/mychatrooms.html', context)


class ChatroomEdit(SuccessMessageMixin, generic.UpdateView):
    model = Chatroom
    fields = ['title', 'description', 'is_anonymous_supported', 'is_private', 'password']
    template_name = 'chatroom/create_chatroom.html'
    success_message = _('Successfully updated')
    success_url = reverse_lazy('mychatrooms')


def delete_chatroom(request, pk):
    chatroom = get_object_or_404(Chatroom, pk=pk)
    chatroom.delete()
    messages.success(request, 'Successfully Deleted!.')
    return redirect("mychatrooms")