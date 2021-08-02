from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Event, EventParticipant


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'address',
            'contact',
            'title',
            'description',
            'start_at',
            'end_at',
            'seats',
            'taken_seats',
            'booked',
            'city'
        ]
        read_only_fields = ['booked', 'taken_seats']