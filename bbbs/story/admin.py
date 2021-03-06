from django.contrib import admin

from bbbs.common.permissions import BaseStaffAdminPermission

from .models import Story


@admin.register(Story)
class RightAdmin(BaseStaffAdminPermission):
    list_display = ('id', 'title', 'child_name', 'friends_since',
                    'show_on_main', 'author', 'added_at',
                    'modified_at', 'intro', 'text', 'quote', 'image'
                    )
    search_fields = ('title', 'child_name',)
    list_filter = ('show_on_main','author',)



