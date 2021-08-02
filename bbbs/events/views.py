from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

#from .filters import EventFilter
from .models import Event, EventParticipant
from .serializers import EventSerializer
#from common.models import Tag
#from common.serializers import TagSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    #pagination_class = EventSetPagination
    #filterset_class = EventFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return Event.event_objects.with_not_finished_for_user(user=user)
        city = self.request.query_params.get('city')
        return Event.event_objects.with_not_finished_for_guest(city=city)

    '''@action(methods=['GET', ], detail=False,
            url_path='tags', url_name='tags')
    def get_tags(self, request):
        tags = Tag.objects.filter(model='event')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)'''


class EventParticipantViewSet(viewsets.ModelViewSet):
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = EventSetPagination

    def get_queryset(self):
        user = self.request.user
        queryset = EventParticipant.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        event_id = self.request.data.get('event')
        event = get_object_or_404(Event, id=event_id)
        if event.takenSeats < event.seats:
            event.takenSeats += 1
            event.save()
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError(
                {'seats': 'Нет доступных мест для регистрации'})

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(),
                                event=self.request.data.get('event'))
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        event = Event.objects.get(pk=instance.event.id)
        event.takenSeats -= 1
        event.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
