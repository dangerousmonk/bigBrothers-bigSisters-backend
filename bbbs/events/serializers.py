from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from bbbs.common.serializers import TagSerializer

from .models import Event, EventParticipant


class EventSerializer(serializers.ModelSerializer):
    taken_seats = serializers.IntegerField(read_only=True)
    booked = serializers.BooleanField(read_only=True)
    tags = TagSerializer(many=True,read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'address',
            'contact',
            'title',
            'description',
            'start_at',
            'end_at',
            'taken_seats',
            'booked',
            'tags'
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
