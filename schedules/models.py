from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Person

# Calender models


class Event(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Done', 'Done'),
        ('Canceled', 'Canceled'),
    )
    status = models.CharField(max_length=20, default='Pending', choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('event_detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


# appointment parts...


class AppointmentSchedule(models.Model):
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Appointments(models.Model):
    appointment_from = models.ForeignKey(Person,related_name='appointment_from', on_delete=models.CASCADE)
    appointment_to = models.ForeignKey(Person,related_name='appointment_to', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Done', 'Done'),
        ('Canceled', 'Canceled'),
    )
    status = models.CharField(max_length=20, default='Pending', choices=STATUS_CHOICES)

