from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from bbbs.common.mixins import ListRetrieveCreateUpdateMixin
from bbbs.common.models import Tag
from bbbs.common.permissions import IsOwnerAdminModeratorOrReadOnly
from bbbs.common.serializers import TagSerializer

from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(ListRetrieveCreateUpdateMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsOwnerAdminModeratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['GET', ], detail=False,
            url_path='tags', url_name='questions-tags')
    def get_tags(self, request):
        tags = Tag.objects.filter(model='questions')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
