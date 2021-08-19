from django.contrib.admin import register
from django.utils.translation import gettext_lazy as _

from bbbs.common.permissions import BaseStaffAdminPermission

from .models import Diary


@register(Diary)
class DiaryAdmin(BaseStaffAdminPermission):
    list_display = (
        'place', 'meeting_date', 'added_at', 'modified_at',
        'description', 'image', 'sent_to_curator', 'mark', 'author'
    )
    search_fields = ('place', 'meeting_date', 'description',)
    list_filter = ('sent_to_curator', 'author', 'mark',)
    empty_value_display = _('empty')

