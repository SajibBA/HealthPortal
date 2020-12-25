from django.urls import path

from . import views

urlpatterns = [
    path(r'calendar', views.CalendarView.as_view(), name='calendar'),
    path(r'event/new/', views.create_event, name='event_new'),
    path(r'event/edit/<int:pk>/', views.EventEdit.as_view(), name='event_edit'),
    path(r'event/<int:event_id>/details/', views.event_details, name='event_detail'),
    path(r'event/<int:event_id>/event_delete/', views.event_delete, name='event_delete'),
    path(r'appointment_calendar', views.AppointmentCalendarView.as_view(), name='appointment_calendar'),
    path(r'create_appointment_schedule/', views.create_appointment_schedule, name='create_appointment_schedule'),
    path(r'view_appointment_schedule/', views.view_appointment_schedule, name='view_appointment_schedule'),
    path(r'delete_appointment_schedule/(?P<pk>\d+)/', views.delete_appointment_schedule,
         name='delete_appointment_schedule'),
    path(r'appointment_schedule/edit/<int:pk>/', views.AppointmentScheduleEdit.as_view(),
         name='appointment_schedule_edit'),
    path(r'appointment_day/(?P<pk>\d+)/', views.appointment_day, name='appointment_day'),
    path(r'appointment_create/(?P<date>\w+)/(?P<schedule_pk>[\w-]+)/$', views.appointment_create,
         name='appointment_create'),


]