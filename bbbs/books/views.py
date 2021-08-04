from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Book
from .serializers import BookSerializer
from bbbs.common.models import Tag
from bbbs.common.serializers import TagSerializer
from .filters import BookFilter
class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filter_class = BookFilter

    @action(methods=['GET', ], detail=False,
            url_path='tags', url_name='book-tags')
    def get_tags(self, request):
        tags = Tag.objects.filter(model='books')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)