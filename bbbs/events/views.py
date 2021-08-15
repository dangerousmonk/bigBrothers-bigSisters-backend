from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bbbs.common.mixins import ListRetreiveCreateDestroyMixin

from .filters import EventFilter
from .models import Event, EventParticipant
from .permissions import IsUserParticipant
from .serializers import EventParticipantSerializer, EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = EventFilter

    def get_queryset(self):
        user = self.request.user
        return Event.event_objects.with_not_finished_for_user(
            user=user, city=user.city
        )

    @action(methods=['GET', ], detail=False,
            url_path='months', url_name='months')
    def get_months(self, request):
        user = request.user
        dates = Event.event_objects.with_not_finished_for_user(
            user=user, city=user.city
        ).dates('start_at', 'month')
        months = [date.month for date in dates]
        return Response(months)

    @action(methods=['GET', ], detail=False,
            url_path='archive', url_name='archive')
    def get_archive(self, request):
        user = request.user
        archived = Event.event_objects.with_finished_for_user(
            user=user, city=user.city
        )
        page = self.paginate_queryset(archived)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(archived, many=True)
        return Response(serializer.data)


class EventParticipantViewSet(ListRetreiveCreateDestroyMixin):
    serializer_class = EventParticipantSerializer
    permission_classes = [IsUserParticipant]

    def get_queryset(self):
        return EventParticipant.participants_objects.not_finished_for_user(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
