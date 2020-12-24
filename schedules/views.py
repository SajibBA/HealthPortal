# cal/views.py

from datetime import datetime, date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta
import calendar
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages


from .models import *
from .utils import Calendar
from .forms import *

# Calender views------------


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calender/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        user = self.request.user
        cal = Calendar(d.year, d.month, user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        status = form.cleaned_data['status']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            status=status,
            end_time = end_time
        )
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'calender/event.html', {'form': form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ['title', 'description', 'start_time', 'end_time', 'status']
    template_name = 'calender/event.html'


def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'calender/event_details.html', context)


def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect("calendar")

#appointment parts----------------------


class AppointmentCalendarView(generic.ListView):
    model = Event
    template_name = 'calender/appointment_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        user = self.request.user
        cal = Calendar(d.year, d.month, user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def create_appointment_schedule(request):
    other_schedule = AppointmentSchedule.objects.filter(creator=request.user)
    form = AppointmentScheduleCreateForm(request.POST or None)
    if request.POST and form.is_valid():
        day = form.cleaned_data['day']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        for other in other_schedule:
            if other.day == day:
                if other.start_time <= start_time <= other.end_time:
                    messages.error(request, "StartTime clash with other schedule!!")
                    return render(request, 'appointment/create_appointment_schedule.html', {'form': form})
                elif other.start_time <= end_time <= other.end_time:
                    messages.error(request, "EndTime clash with other schedule!!")
                    return render(request, 'appointment/create_appointment_schedule.html', {'form': form})
        AppointmentSchedule.objects.get_or_create(
            creator=request.user,
            day=day,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('profile_home'))
    return render(request, 'appointment/create_appointment_schedule.html', {'form': form})


def view_appointment_schedule(request):
    appointment_schedule = AppointmentSchedule.objects.filter(creator=request.user)
    sat = 0
    sun = 0
    mon = 0
    tue = 0
    wed = 0
    thus = 0
    fri = 0
    for appoint in appointment_schedule:
        if appoint.day == 'Saturday':
            if sat == 0:
                sat = 1
            sat = sat+1
        elif appoint.day == 'Sunday':
            if sun == 0:
                sun = 1
            sun = sun+1
        elif appoint.day == 'Monday':
            if mon == 0:
                mon = 1
            mon = mon+1
        elif appoint.day == 'Tuesday':
            if tue == 0:
                tue = 1
            tue = tue+1
        elif appoint.day == 'Wednesday':
            if wed == 0:
                wed = 1
            wed = wed+1
        elif appoint.day == 'Thursday':
            if thus == 0:
                thus = 1
            thus = thus+1
        elif appoint.day == 'Friday':
            if fri == 0:
                fri = 1
            fri = fri+1
    context = {'appointment_schedule': appointment_schedule, 'sat': sat, 'sun': sun, 'mon': mon, 'tue': tue, 'wed': wed, 'thus': thus, 'fri': fri}
    return render(request, 'appointment/view_appointment_schedule.html', context)


class AppointmentScheduleEdit(generic.UpdateView):
    model = AppointmentSchedule
    fields = ['day', 'start_time', 'end_time']
    template_name = 'appointment/create_appointment_schedule.html'
    success_url = reverse_lazy('view_appointment_schedule')


def delete_appointment_schedule(request, pk):
    appointment_schedule = get_object_or_404(AppointmentSchedule, pk=pk)
    appointment_schedule.delete()
    return redirect("view_appointment_schedule")