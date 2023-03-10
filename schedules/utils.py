# /utils.py

from calendar import HTMLCalendar

from .models import Event, Appointments


#from eventcalendar.helper import get_current_user


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            if event.status == 'Done':
                d += f'<li> {event.get_html_url}<i class="fa fa-check-circle-o" style="color:green" aria-hidden="true"></i></li>'
            elif event.status == 'Canceled':
                d += f'<li> {event.get_html_url}<i class="fa fa-ban" style="color:red" aria-hidden="true"></i></li>'
            else:
                d += f'<li> {event.get_html_url}<i class="fa fa-refresh" style="color:blue" aria-hidden="true"></i></li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d}</ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, user=self.user)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal

#calender for appointment------------(not functional)


class AppointmentCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(AppointmentCalendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            if event.status == 'Done':
                d += f'<li> {event.get_html_url}<i class="fa fa-check-circle-o" style="color:green" aria-hidden="true"></i></li>'
            elif event.status == 'Canceled':
                d += f'<li> {event.get_html_url}<i class="fa fa-ban" style="color:red" aria-hidden="true"></i></li>'
            else:
                d += f'<li> {event.get_html_url}<i class="fa fa-refresh" style="color:blue" aria-hidden="true"></i></li>'
        if day != 0:
            return f"<td><span class='date'>{day}hola</span><ul> {d}</ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Appointments.objects.filter(date__year=self.year, date__month=self.month, appointment_from=self.user)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
