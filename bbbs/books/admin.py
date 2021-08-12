from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy as _

from bbbs.common.models import Tag

from .models import Book


@register(Book)
class BookAdmin(ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'year', 'description', 'color',
        'url', 'added_at', 'get_tags',
    )
    readonly_fields = []

    search_fields = ('author', 'title',)
    list_filter = ('year', 'author', 'color')
    empty_value_display = _('empty')

    @admin.display(description=_('tags'))
    def get_tags(self, obj):
        qs = obj.list_tags()
        if qs:
            return list(qs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            kwargs['queryset'] = Tag.objects.filter(model='books')
        return super().formfield_for_manytomany(db_field, request, **kwargs)
