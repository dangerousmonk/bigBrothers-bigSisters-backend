from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Event, EventParticipant


class EventSerializer(serializers.ModelSerializer):
    taken_seats = serializers.IntegerField(read_only=True)
    booked = serializers.BooleanField(read_only=True)

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


class EventParticipantSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = EventParticipant
        fields = ['id', 'event', 'user']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=EventParticipant.objects.all(),
                fields=['user', 'event'],
                message=_('You already registered for this event'),
            )
        ]
