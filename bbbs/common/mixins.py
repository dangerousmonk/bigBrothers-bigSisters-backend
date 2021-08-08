from rest_framework import mixins
from rest_framework import viewsets


class ListRetrieveCreateUpdateMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass
