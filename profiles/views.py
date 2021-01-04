from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views import generic
from datetime import datetime as date

from schedules.models import AppointmentSchedule, Appointments
from .filters import *

from .decorators import *
from .forms import *
from .models import *
# Create your views here.


def home(request):
    return render(request, 'home.html')



# Registration and login------------


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class Login(TemplateView):
    template_name = 'registration/login.html'


class NormalSignUpView(SuccessMessageMixin, CreateView):
    model = Person
    form_class = NormalSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'normal'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class ProfessionalSignUpView(SuccessMessageMixin, CreateView):
    model = Person
    form_class = ProfessionalSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'professional'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


# Profile Homepage------------


def profile_home(request):
    message = Message.objects.filter(sent_to=request.user)
    if request.user.is_normal:
        appointment = Appointments.objects.filter(appointment_from=request.user, date=date.today())
    else:
        appointment = Appointments.objects.filter(appointment_to=request.user, date=date.today())
    flag = 0                                # ---For Notifications
    flag2 = 0
    flag_appointment = 0
    for messa in message:
        if messa.mark_as_read == 0:
            flag = 1
            break
    for mess in message:
        if mess.mark_as_read == 0:
            flag2 = flag2 + 1
    for app in appointment:
        if app.status == 'Pending':
            flag_appointment = flag_appointment + 1

    ratings = Ratings.objects.filter(rate_to=request.user)
    rates = 0
    rater = 0
    for rate in ratings:
        rater = rater + 1
        rates = rates + rate.rating
    try:
        final_rating = rates / rater
    except ZeroDivisionError:
        final_rating = 0
    final_rating = round(final_rating, 2)
    reviews = Ratings.objects.filter(rate_to=request.user)
    context = {'flag': flag, 'flag2': flag2, 'flag_appointment': flag_appointment,
               'final_rating': final_rating, 'reviews': reviews, 'rater': rater}
    return render(request, 'profile_home.html', context)


# Profile Details------------

def profile(request):
    return render(request, 'registration/profile.html')

# Profile edit------------


class NormalProfileEditView(SuccessMessageMixin, UpdateView):
    form_class = NormalProfileEditForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('profile')
    success_message = _('Profile successfully updated')

    def get_object(self):
        return self.request.user


class ProfessionalProfileEditView(SuccessMessageMixin, UpdateView):
    form_class = ProfessionalProfileEditForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('profile')
    success_message = _('Profile successfully updated')

    def get_object(self):
        return self.request.user

# Password Change------------


class ProfilePasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('profile_home')


# About person details------------

def add_about(request):
    form = AboutForm(request.POST, request.FILES or None)
    if request.POST and form.is_valid():
        info = form.cleaned_data['info']
        AboutProfessional.objects.get_or_create(
            person=request.user,
            info=info,
        )
        messages.success(request, 'About Successfully Added!')
        return HttpResponseRedirect(reverse('profile'))
    return render(request, 'add_about.html', {'form': form})


class AboutEdit(SuccessMessageMixin, generic.UpdateView):
    model = AboutProfessional
    fields = ['info']
    template_name = 'add_about.html'
    success_message = _('Successfully updated')
    success_url = reverse_lazy('profile')


# View others profile------------


def view_professionals(request):
    person = Person.objects.all()
    myFilter = PersonFilter(request.GET, queryset=person)
    person = myFilter.qs
    context = {'person': person, 'myFilter': myFilter}
    return render(request, 'view_professionals.html', context)


def view_professionals_profile(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        raise Http404
    appointment_schedule = AppointmentSchedule.objects.filter(creator=person)
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
            sat = sat + 1
        elif appoint.day == 'Sunday':
            if sun == 0:
                sun = 1
            sun = sun + 1
        elif appoint.day == 'Monday':
            if mon == 0:
                mon = 1
            mon = mon + 1
        elif appoint.day == 'Tuesday':
            if tue == 0:
                tue = 1
            tue = tue + 1
        elif appoint.day == 'Wednesday':
            if wed == 0:
                wed = 1
            wed = wed + 1
        elif appoint.day == 'Thursday':
            if thus == 0:
                thus = 1
            thus = thus + 1
        elif appoint.day == 'Friday':
            if fri == 0:
                fri = 1
            fri = fri + 1

    ratings = Ratings.objects.filter(rate_to=person)
    rates = 0
    rater = 0
    for rate in ratings:
        rater = rater+1
        rates = rates+rate.rating
    try:
        final_rating = rates / rater
    except ZeroDivisionError:
        final_rating = 0
    final_rating = round(final_rating, 2)
    form_rate = RatingForm(request.POST or None)
    rate_from = request.user
    rate_to = person
    given_rating = Ratings.objects.filter(rate_from=rate_from, rate_to=rate_to)
    reviews = Ratings.objects.filter(rate_to=rate_to)
    achievements = Achievements.objects.filter(holder=person)
    if request.POST and form_rate.is_valid():
        if '_rate' in request.POST:
            rating = request.POST['rating']
            review = request.POST['review']
            if len(given_rating) == 0:
                given_rating = Ratings.objects.get_or_create(
                    rate_from=rate_from,
                    rating=rating,
                    review=review,
                    rate_to=rate_to
                )
            else:
                given_rating = Ratings.objects.filter(rate_from=rate_from, rate_to=rate_to).update(
                    rate_from=rate_from,
                    rating=rating,
                    review=review,
                    rate_to=rate_to
                )
            context = {'appointment_schedule': appointment_schedule, 'sat': sat, 'sun': sun, 'mon': mon, 'tue': tue,
                       'wed': wed,
                       'thus': thus, 'fri': fri, 'person': person, 'final_rating': final_rating, 'rater': rater,
                       'given_rating': given_rating, 'reviews': reviews,
                       "achievements": achievements}
            return render(request, 'view_professionals_profile.html', context)
        else:
            context = {'appointment_schedule': appointment_schedule, 'sat': sat, 'sun': sun, 'mon': mon, 'tue': tue,
                       'wed': wed,
                       'thus': thus, 'fri': fri, 'person': person, 'final_rating': final_rating, 'rater': rater,
                       'form_rate': form_rate, 'reviews': reviews,
                       "achievements": achievements}
            return render(request, 'view_professionals_profile.html', context)
    else:
        context = {'appointment_schedule': appointment_schedule, 'sat': sat, 'sun': sun, 'mon': mon, 'tue': tue,
                   'wed': wed,
                   'thus': thus, 'fri': fri, 'person': person, 'final_rating': final_rating, 'rater': rater,
                   'form_rate': form_rate, 'reviews': reviews,
                   "achievements": achievements}
        return render(request, 'view_professionals_profile.html', context)


def search_professionals(request):
    professional = Professional.objects.all()
    myFilter = ProfessionFilter(request.GET, queryset=professional)
    professional = myFilter.qs
    context = {'professional': professional, 'myFilter': myFilter}
    return render(request, 'search_professionals.html', context)


# Message Part.............


def send_message(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        raise Http404

    if request.method =='POST':
        message_details = request.POST['message_details']
        sent_from = request.user
        sent_to = person
        message = Message.objects.create(
            message_details=message_details,
            sent_from=sent_from,
            sent_to=sent_to
        )
        context = {'person': person, 'message': message}
        return render(request, 'send_message.html', context)
    else:
        return render(request, 'send_message.html', {'person': person})


def view_messages(request):
    message = Message.objects.filter(sent_to=request.user)
    myFilter = MessageFilter(request.GET, queryset=message)
    message = myFilter.qs
    context = {'message': message, 'myFilter': myFilter}
    return render(request, 'view_messages.html', context)


def update_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.mark_as_read == True:
        message = Message.objects.filter(pk=pk).update(mark_as_read='False')
    else:
        message = Message.objects.filter(pk=pk).update(mark_as_read='True')
    return redirect("view_messages")


def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.delete()
    return redirect("view_messages")

# Feedbacks------------


def feedback(request):
    form = FeedbackForm(request.POST or None)
    if request.POST and form.is_valid():
        message_details = request.POST['message_details']
        feedback_from = request.user
        type = form.cleaned_data['type']
        priority = form.cleaned_data['priority']
        feed = Feedback.objects.create(
            message_details=message_details,
            feedback_from=feedback_from,
            type=type,
            priority=priority,
        )
        context = {'feed': feed, 'form': form}
        messages.success(request, 'Thanks for your valuable feedback/report ')
        return render(request, 'profile_home.html', context)
    else:
        context = {'form': form}
        return render(request, 'feedback.html', context)


# Achievements------------

def add_achievements(request):
    form = AchievementsForm(request.POST, request.FILES or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        details = form.cleaned_data['details']

        Achievements.objects.get_or_create(
            holder=request.user,
            title=title,
            details=details,
            achievement_pic=form.cleaned_data['achievement_pic']
        )
        messages.success(request, 'Achievements Successfully Added!')
        return HttpResponseRedirect(reverse('view_achievements'))
    return render(request, 'add_achievements.html', {'form': form})


def view_achievements(request):
    achievements = Achievements.objects.filter(holder=request.user)
    return render(request, 'view_achievements.html', {'achievements': achievements})


class AchievementsEdit(SuccessMessageMixin, generic.UpdateView):
    model = Achievements
    fields = ['title', 'details', 'achievement_pic']
    template_name = 'add_achievements.html'
    success_message = _('Successfully updated')
    success_url = reverse_lazy('view_achievements')


def delete_achievements(request, pk):
    achievements = get_object_or_404(Achievements, pk=pk)
    achievements.delete()
    messages.success(request, 'Successfully Deleted!.')
    return redirect("view_achievements")