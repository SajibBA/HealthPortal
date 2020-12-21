from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.forms.utils import ValidationError

from .models import *


class ProfessionalSignUpForm(UserCreationForm):
    profession = forms.CharField(
        required=True
    )
    speciality = forms.CharField(
        required=True
    )
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta(UserCreationForm.Meta):
        model = Person
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'gender',
            'date_of_birth',
            'profile_pic',
            'address',
            'profession',
            'speciality',

        ]



    @transaction.atomic
    def save(self, commit=True):
        person = super().save(commit=False)
        person.is_professional = True
        person.save()
        professional = Professional.objects.create(person=person, profession=self.cleaned_data.get('profession'),
                                                   speciality=self.cleaned_data.get('speciality'))
        return person


class NormalSignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta(UserCreationForm.Meta):
        model = Person
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'gender',
            'date_of_birth',
            'profile_pic',
            'address',

        ]

    @transaction.atomic
    def save(self,  commit=True):
        person = super().save(commit=False)
        person.is_normal = True
        person.save()
        normal = Normal.objects.create(person=person)
        return person


class NormalProfileEditForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Person
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'gender',
            'date_of_birth',
            'profile_pic',
            'address',

        ]
        date_of_birth = forms.DateField(
            widget=forms.TextInput(
                attrs={'type': 'date'}
            )
        )

    @transaction.atomic
    def save(self,  commit=True):
        person = super().save(commit=False)
        person.is_normal = True
        person.save()
        normal = Normal.objects.filter(person=person)
        return person


class ProfessionalProfileEditForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Person
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'gender',
            'date_of_birth',
            'profile_pic',
            'address',
            'profession',
            'speciality',
        ]
    profession = forms.CharField(
        required=True
    )
    speciality = forms.CharField(
        required=True
    )
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    @transaction.atomic
    def save(self, commit=True):
        person = super().save(commit=False)
        person.is_professional = True
        person.save()
        professional = Professional.objects.filter(person=person).update(profession=self.cleaned_data.get('profession'),
                                                                         speciality=self.cleaned_data.get('speciality'))
        return person

