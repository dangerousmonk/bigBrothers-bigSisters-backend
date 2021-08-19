from django.contrib.admin import register
from django.utils.translation import gettext_lazy as _

from bbbs.common.permissions import BaseStaffAdminPermission

from .models import Article


@register(Article)
class ArticleAdmin(BaseStaffAdminPermission):
    list_display = (
        'id', 'title', 'author_info', 'article_url', 'content', 'image',
        'show_on_main', 'added_at',
    )
    search_fields = ('title', 'author_info')
    list_filter = ('show_on_main',)
    empty_value_display = _('empty')
