from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bbbs.common.models import Tag
from bbbs.common.serializers import TagSerializer

from .filters import VideoFilter
from .models import Video, Movie
from .serializers import VideoSerializer, MovieSerializer


class VideoViewSet(ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]
    filter_class = VideoFilter

    @action(methods=['GET', ], detail=False,
            url_path='tags', url_name='tags')
    def get_tags(self, request):
        tags = Tag.objects.filter(model='videos')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class MovieViewSet(ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    @action(methods=['GET', ], detail=False,
            url_path='tags', url_name='tags')
    def get_tags(self, request):
        tags = Tag.objects.filter(model='movies')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

