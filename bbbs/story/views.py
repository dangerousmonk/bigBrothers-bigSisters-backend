from bbbs.common.mixins import ListRetrieveCreateUpdateMixin
from bbbs.common.permissions import IsOwnerAdminModeratorOrReadOnly

from .models import Story
from .serializers import StorySerializer


class StoryViewSet(ListRetrieveCreateUpdateMixin):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsOwnerAdminModeratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
