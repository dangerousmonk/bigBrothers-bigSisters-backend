from django.contrib.admin import register
from django.utils.translation import gettext_lazy as _

from bbbs.common.mixins import TagAdminMixin
from bbbs.common.permissions import BaseStaffAdminPermission

from .models import Question


@register(Question)
class QuestionAdmin(BaseStaffAdminPermission, TagAdminMixin):
    list_display = (
        'id', 'question', 'answer', 'added_at', 'modified_at', 'show_on_main',
        'get_tags',
        'author'
    )
    search_fields = ('question', 'answer', 'added_at')
    list_filter = ('author', 'show_on_main', 'added_at')
    ordering = ('-added_at',)
    empty_value_display = _('empty')
