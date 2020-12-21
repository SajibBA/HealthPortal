from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404
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
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
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
    for message in message:
        if message.mark_as_read == 0:
            flag = 1
            break
    context = {'flag': flag}
    return render(request, 'profile_home.html', context)


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class Login(TemplateView):
    template_name = 'registration/login.html'


class NormalSignUpView(CreateView):
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


class ProfessionalSignUpView(CreateView):
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


class NormalProfileEditView(UpdateView):
    form_class = NormalProfileEditForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class ProfessionalProfileEditView(UpdateView):
    form_class = ProfessionalProfileEditForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class ProfilePasswordChangeView(PasswordChangeView):
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
    return render(request, 'view_professionals_profile.html', {'person': person})


def search_professionals(request):
    professional = Professional.objects.all()
    myFilter = ProfessionFilter(request.GET, queryset=professional)
    professional = myFilter.qs
    context = {'professional': professional, 'myFilter': myFilter}
    return render(request, 'search_professionals.html', context)


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