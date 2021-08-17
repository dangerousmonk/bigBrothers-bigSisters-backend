from django_filters import rest_framework as filters

from bbbs.common.models import Tag

from .models import Video


class VideoFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Video
        fields = ['tags',]
