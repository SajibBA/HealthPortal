from django.urls import path

from . import views

urlpatterns = [
    path(r'create_chatroom/', views.create_chatroom,
         name='create_chatroom'),
    path(r'view_chatroom/', views.view_chatroom,
         name='view_chatroom'),
    path(r'live_chatroom/(?P<pk>\d+)/', views.live_chatroom, name='live_chatroom'),
    path(r'protected_chatroom/(?P<pk>\d+)/', views.protected_chatroom, name='protected_chatroom'),
    path(r'join_chatroom/(?P<pk>\d+)/', views.join_chatroom, name='join_chatroom'),
    path(r'anonymous_chatroom/(?P<pk>\d+)/', views.anonymous_chatroom, name='anonymous_chatroom'),


]