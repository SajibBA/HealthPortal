import django_filters
from django import forms

from .models import *


class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            'username',
            'first_name',

        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
            models.DateTimeField: {
                'filter_class': django_filters.IsoDateTimeFilter
            },
        }



class ProfessionFilter(django_filters.FilterSet):
    class Meta:
        model = Professional
        fields = [
            'person__username',
            'person__first_name',
            'profession',
            'speciality',
      ]


class MessageFilter(django_filters.FilterSet):
    sent_at = django_filters.IsoDateTimeFilter()

    class Meta:
        model = Message
        fields = [
          'sent_from',
          'sent_at',
          'mark_as_read',

        ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
            models.DateTimeField: {
                'filter_class': django_filters.IsoDateTimeFilter,
            },
        }


