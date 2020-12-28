from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.forms import ModelForm
from django.forms.utils import ValidationError
from django.utils.translation import ugettext as _
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

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date_of_birth



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

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date_of_birth

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

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date_of_birth

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

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date_of_birth

    @transaction.atomic
    def save(self, commit=True):
        person = super().save(commit=False)
        person.is_professional = True
        person.save()
        professional = Professional.objects.filter(person=person).update(profession=self.cleaned_data.get('profession'),
                                                                         speciality=self.cleaned_data.get('speciality'))
        return person


class RatingForm(ModelForm):

    class Meta:
        model = Ratings
        fields = [
            'rating',
            'review',
        ]


class FeedbackForm(ModelForm):

    class Meta:
        model = Feedback
        fields = [
            'type',
            'priority',

        ]


class AchievementsForm(ModelForm):

    class Meta:
        model = Achievements
        fields = [
            'title',
            'details',
            'achievement_pic',

        ]
