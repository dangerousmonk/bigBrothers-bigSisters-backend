from rest_framework.routers import DefaultRouter

from bbbs.events.views import EventViewSet, EventParticipantViewSet


v1_router = DefaultRouter()
v1_router.register(r'afisha/events', EventViewSet, basename='events')
v1_router.register(r'afisha/event-participants', EventParticipantViewSet, basename='event-participants')
