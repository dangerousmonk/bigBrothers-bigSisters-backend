from rest_framework.routers import DefaultRouter

from bbbs.articles.views import ArticleViewSet
from bbbs.books.views import BookViewSet
from bbbs.common.views import CityViewSet
from bbbs.events.views import EventParticipantViewSet, EventViewSet
from bbbs.rights.views import RightViewSet
from bbbs.questions.views import QuestionViewSet

v1_router = DefaultRouter()
v1_router.register(r'afisha/events', EventViewSet, basename='events')
v1_router.register(r'afisha/event-participants', EventParticipantViewSet, basename='event-participants')
v1_router.register(r'articles', ArticleViewSet, basename='articles')
v1_router.register(r'books', BookViewSet, basename='books')
v1_router.register(r'rights', RightViewSet, basename='rights')
v1_router.register(r'cities', CityViewSet, basename='cities')
v1_router.register(r'questions', QuestionViewSet, basename='questions')
