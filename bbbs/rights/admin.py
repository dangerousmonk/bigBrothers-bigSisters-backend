from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from bbbs.common.mixins import TagAdminMixin
from bbbs.common.permissions import BaseStaffAdminPermission

from .models import Right


@admin.register(Right)
class RightAdmin(BaseStaffAdminPermission, TagAdminMixin):
    list_display = ('id', 'title', 'get_description', 'get_tags')
    search_fields = ('title', 'description', 'text')
    list_filter = ('tags','color',)

    @admin.display(description=_('description'))
    def get_description(self, obj):
        description = obj.description
        if description is not None:
            return f'{description[:30]}...'
        return description

