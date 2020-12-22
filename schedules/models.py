from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Person


class Event(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('event_detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


