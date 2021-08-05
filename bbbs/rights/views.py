from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bbbs.common.models import Tag
from bbbs.common.serializers import TagSerializer

from .models import Right
from .serializers import RightSerializer


class RightViewSet(ReadOnlyModelViewSet):
    queryset = Right.objects.all()
    serializer_class = RightSerializer
    permission_classes = [AllowAny]

    @action(methods=['GET', ], detail=False,
            url_path='tags', url_name='rights-tags')
    def get_tags(self, request):
        tags = Tag.objects.filter(model='rights')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
