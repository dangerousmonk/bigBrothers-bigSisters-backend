from rest_framework.routers import DefaultRouter

from bbbs.events.views import EventViewSet, EventParticipantViewSet
from bbbs.articles.views import ArticleViewSet
from bbbs.books.views import BookViewSet


v1_router = DefaultRouter()
v1_router.register(r'afisha/events', EventViewSet, basename='events')
v1_router.register(r'afisha/event-participants', EventParticipantViewSet, basename='event-participants')
v1_router.register(r'articles', ArticleViewSet, basename='articles')
v1_router.register(r'books', BookViewSet, basename='books')