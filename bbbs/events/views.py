from django.shortcuts import get_object_or_404

from rest_framework import (generics, mixins, permissions, serializers, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, EventParticipant
from .serializers import EventParticipantSerializer, EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny] # TODO: Change back to only authenticated
    #pagination_class = LimitOffsetPagination
    #filterset_class = EventFilter


    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return Event.event_objects.with_not_finished_for_user(user=user,city=user.city)
        city = self.request.query_params.get('city')
        return Event.event_objects.with_not_finished_for_guest(city=city)

    '''@action(methods=['GET', ], detail=False,
            url_path='tags', url_name='tags')
    def get_tags(self, request):
        tags = Tag.objects.filter(model='event')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)'''


class EventParticipantViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    #permission_classes = [permissions.IsAuthenticated]
    #pagination_class = EventSetPagination

    def get_queryset(self):
        return EventParticipant.objects.all()
        #user = self.request.user
        #queryset = EventParticipant.objects.filter(user=user)
        #return queryset

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
