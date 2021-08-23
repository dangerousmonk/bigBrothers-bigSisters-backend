from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy as _

from .models import City, Region, Tag


@register(City)
class CityAdmin(ModelAdmin):
    list_display = (
        'id', 'name', 'is_primary',)

    search_fields = ('name',)
    list_filter = ('is_primary',)
    empty_value_display = _('empty')


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        'id', 'name', 'slug', 'model',)
    search_fields = ('name', 'model',)
    list_filter = ('model',)
    empty_value_display = _('empty')


@register(Region)
class RegionAdmin(ModelAdmin):
    list_display = (
        'id', 'name', 'code_iso_3166', 'timezone')
    search_fields = ('name',)
    list_filter = ('timezone',)
    empty_value_display = _('empty')
