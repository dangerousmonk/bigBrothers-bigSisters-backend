from django_filters import CharFilter, FilterSet

from .models import Event


class EventFilter(FilterSet):
    months = CharFilter(field_name='start_at', method='filter_months')

    def filter_months(self, queryset, name, months):
        lookup = '__'.join([name, 'month__in'])
        return queryset.filter(**{lookup: months.split(',')})

    class Meta:
        model = Event
        fields = ['months', ]
