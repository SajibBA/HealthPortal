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

from schedules.models import AppointmentSchedule
from .filters import *

from .decorators import *
from .forms import *
from .models import *
# Create your views here.


def home(request):
    return render(request, 'home.html')


def profile(request):
    return render(request, 'registration/profile.html')


def profile_home(request):
    message = Message.objects.filter(sent_to=request.user)
    flag = 0
    flag2 = 0
    for messa in message:
        if messa.mark_as_read == 0:
            flag = 1
            break
    for mess in message:
        if mess.mark_as_read == 0:
            flag2 = flag2 + 1
    context = {'flag': flag, 'flag2': flag2}
    return render(request, 'profile_home.html', context)


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


class ProfilePasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('profile_home')



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
                       'given_rating': given_rating, 'reviews': reviews}
            return render(request, 'view_professionals_profile.html', context)
        else:
            context = {'appointment_schedule': appointment_schedule, 'sat': sat, 'sun': sun, 'mon': mon, 'tue': tue,
                       'wed': wed,
                       'thus': thus, 'fri': fri, 'person': person, 'final_rating': final_rating, 'rater': rater,
                       'form_rate': form_rate, 'reviews': reviews}
            return render(request, 'view_professionals_profile.html', context)
    else:
        context = {'appointment_schedule': appointment_schedule, 'sat': sat, 'sun': sun, 'mon': mon, 'tue': tue,
                   'wed': wed,
                   'thus': thus, 'fri': fri, 'person': person, 'final_rating': final_rating, 'rater': rater,
                   'form_rate': form_rate, 'reviews': reviews}
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

