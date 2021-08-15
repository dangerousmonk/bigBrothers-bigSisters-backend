from django_filters import rest_framework as filters

from bbbs.common.models import Tag

from .models import Place


class PlaceFilter(filters.FilterSet):
    min_age = filters.NumberFilter(field_name='age', lookup_expr='gte')
    max_age = filters.NumberFilter(field_name='age', lookup_expr='lte')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    chosen = filters.BooleanFilter(field_name='chosen')

    class Meta:
        model = Place
        fields = ['age', 'tags', 'chosen']
