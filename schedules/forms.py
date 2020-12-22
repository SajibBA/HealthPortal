from django.forms import ModelForm, DateInput
from datetime import datetime, date
from .models import Event
from django import forms

# Calender forms


class EventForm(ModelForm):
  start_time = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}
        ))
  end_time = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}
        ))

  class Meta:
    model = Event
    exclude = ['user']


#



