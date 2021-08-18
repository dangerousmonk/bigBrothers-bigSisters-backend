from rest_framework.decorators import action
from rest_framework.response import Response

from bbbs.common.mixins import ListRetrieveCreateUpdateMixin
from bbbs.common.models import Tag
from bbbs.common.permissions import IsOwnerAdminModeratorOrReadOnly
from bbbs.common.serializers import TagSerializer

from .filters import PlaceFilter
from .models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(ListRetrieveCreateUpdateMixin):
    serializer_class = PlaceSerializer
    filterset_class = PlaceFilter
    permission_classes = [IsOwnerAdminModeratorOrReadOnly]

    def get_queryset(self):
        qs = Place.objects.exclude(verified=False)
        user = self.request.user
        if user.is_authenticated:
            return qs.filter(city=user.city)
        city = self.request.data.get('city')
        if city is not None:
            return qs.filter(city=city)
        return qs

    def perform_create(self, serializer):
        serializer.save(
            chosen=self.request.user.is_mentor,
            city=self.request.user.city,
            author=self.request.user
        )

    @action(methods=['GET', ], detail=False,
            url_path='chosen', url_name='chosen')
    def get_chosen(self, request):
        chosen_place = self.get_queryset().order_by('-chosen').first()
        serializer = self.get_serializer(chosen_place)
        return Response(serializer.data)

    @action(methods=['GET', ], detail=False,
            url_path='tags', url_name='tags')
    def get_tags(self, request):
        tags = Tag.objects.filter(model='places')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

