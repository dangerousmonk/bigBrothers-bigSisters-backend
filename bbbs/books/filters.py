from django_filters import rest_framework as filters
from .models import Book
from bbbs.common.models import Tag
class BookFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    class Meta:
        model = Book
        fields = ['tags',]
