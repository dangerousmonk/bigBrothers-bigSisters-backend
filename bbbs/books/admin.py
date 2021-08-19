from django.contrib.admin import register
from django.utils.translation import gettext_lazy as _

from bbbs.common.mixins import TagAdminMixin

from .models import Book


@register(Book)
class BookAdmin(TagAdminMixin):
    list_display = (
        'id', 'title', 'author', 'year', 'description', 'color',
        'url', 'added_at', 'get_tags',
    )
    search_fields = ('author', 'title',)
    list_filter = ('year', 'author', 'color')
    empty_value_display = _('empty')
