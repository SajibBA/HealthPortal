from django.contrib import admin
from .models import *
from schedules.models import *

# Register your models here.

admin.site.register(Person)
admin.site.register(AppointmentSchedule)