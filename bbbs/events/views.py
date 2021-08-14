from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bbbs.common.mixins import ListRetreiveCreateDestroyMixin

from .filters import EventFilter
from .models import Event, EventParticipant
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
        serializer = EventSerializer(archived, many=True)
        return Response(serializer.data)




class EventParticipantViewSet(ListRetreiveCreateDestroyMixin):
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer

    # permission_classes = [permissions.IsAuthenticated]
    # pagination_class = EventSetPagination

    def get_queryset(self):
        return EventParticipant.objects.all()
        # user = self.request.user
        # queryset = EventParticipant.objects.filter(user=user)
        # return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(),
                                event=self.request.data.get('event'))
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        event = Event.objects.get(pk=instance.event.id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
