from django.contrib.admin import register
from django.utils.translation import gettext_lazy as _

from bbbs.common.mixins import RegModeratorAdminMixin, TagAdminMixin

from .models import Place


@register(Place)
class EventAdmin(TagAdminMixin, RegModeratorAdminMixin):
    list_display = ('id', 'title', 'address', 'city',
                    'gender', 'age', 'activity_type',
                    'pub_date', 'author',
                    'get_tags',
                    'chosen', 'verified', 'show_on_main'
                    )
    search_fields = ('title', 'address',)
    list_filter = ('city', 'gender', 'age',
                   'activity_type', 'author',
                   'chosen', 'verified', 'show_on_main'
                   )
    ordering = ('-pub_date',)
    empty_value_display = _('-empty-')
