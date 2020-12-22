from django.urls import path

from . import views

urlpatterns = [
    path(r'calendar', views.CalendarView.as_view(), name='calendar'),
    path(r'event/new/', views.create_event, name='event_new'),
    path(r'event/edit/<int:pk>/', views.EventEdit.as_view(), name='event_edit'),
    path(r'event/<int:event_id>/details/', views.event_details, name='event_detail'),
    path(r'event/<int:event_id>/event_delete/', views.event_delete, name='event_delete'),
]