import django_filters
from django import forms

from .models import *


class ChatroomFilter(django_filters.FilterSet):

    class Meta:
        model = Chatroom
        fields = {
            'title',
            'creator',
            'is_anonymous_supported',
            'is_private',
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