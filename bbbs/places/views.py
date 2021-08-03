from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from .serializers import PlaceReadSerializer, PlaceWriteSerializer
from .models import Place
from common.models import Profile, Tag
from common.serializers import TagSerializer
from .filters import PlacesFilter
from .pagination import PlaceSetPagination


class CustomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Pk lookup not allowed
    """
    pass


class PlacesListViewSet(CustomViewSet):
    serializer_class = PlaceReadSerializer
    filterset_class = PlacesFilter
    pagination_class = PlaceSetPagination

    def get_queryset(self):
        # Отдаем фронту все места, кроме последнего
        # добавленного наставником, последнее - для большой карточки
        # фронт его получает из api/v1/place/?city={id}
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)
            city = profile.city
        else:
            city = self.request.query_params.get('city')
        latest = Place.objects.filter(
            verified=True,
            chosen=True,
            city=city
        ).first()
        if latest:
            return Place.objects.filter(city=city, verified=True).exclude(id=latest.id)
        return Place.objects.filter(city=city, verified=True)

    @action(methods=['GET', ], detail=False,
            url_path='tags', url_name='tags')
    def get_tags(self, request):
        tags = Tag.objects.filter(model='place')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class PlaceRetrieveCreate(RetrieveAPIView, CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlaceReadSerializer
        return PlaceWriteSerializer

    def get_object(self):
        city = self.request.query_params.get('city')
        try:
            latest_chosen = Place.objects.filter(
                verified=True,
                chosen=True,
                city=city
            ).latest('pubDate')
            return latest_chosen
        except ObjectDoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        serializer.save(chosen=self.request.user.is_mentor)