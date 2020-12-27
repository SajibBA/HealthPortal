from django.contrib import admin

from chatapp.models import *
from .models import *
from schedules.models import *

# Register your models here.

admin.site.register(Person)
admin.site.register(AppointmentSchedule)
admin.site.register(Appointments)
admin.site.register(Ratings)
admin.site.register(Chatroom)
admin.site.register(Chats)
admin.site.register(Feedback)
admin.site.register(Message)
