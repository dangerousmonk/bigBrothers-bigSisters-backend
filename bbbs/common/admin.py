from .models import City, Tag

from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy as _


@register(City)
class CityAdmin(ModelAdmin):
    list_display = (
        'id', 'name', 'is_primary',)
    readonly_fields = []


    search_fields = ('name',)
    list_filter = ('is_primary',)
    empty_value_display = _('empty')


@register(Tag)
class BookAdmin(ModelAdmin):
    list_display = (
        'id', 'name', 'slug', 'model',)
    readonly_fields = []
    search_fields = ('name', 'model',)
    list_filter = ('model',)
    empty_value_display = _('empty')

