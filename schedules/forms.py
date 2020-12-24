from django.forms import ModelForm, DateInput
from datetime import datetime, date
from .models import *
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


# Appointments .....


class AppointmentScheduleCreateForm(ModelForm):

    class Meta:
        model = AppointmentSchedule
        exclude = ['creator']

    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}
                                                        ))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}
                                                      ))

    def clean(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if start_time > end_time:
            raise forms.ValidationError("StartTime must be earlier than the EndTime!!")

