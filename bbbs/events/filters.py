from django_filters import rest_framework as filters

from .models import Event


class EventFilter(filters.FilterSet):
    months = filters.CharFilter(field_name='start_at', method='filter_months')

    def filter_months(self, queryset, name, months):
        lookup = '__'.join([name, 'month__in'])
        return queryset.filter(**{lookup: months.split(',')})

    class Meta:
        model = Event
        fields = ['months', ]
