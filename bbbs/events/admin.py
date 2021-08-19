from django.contrib import admin
from django.contrib.admin import register

from .models import Event, EventParticipant

admin.site.register(EventParticipant)
from bbbs.common.mixins import RegModeratorAdminMixin, TagAdminMixin


@register(Event)
class EventAdmin(TagAdminMixin, RegModeratorAdminMixin):
    list_display = (
        'city', 'title', 'start_at',
        'end_at', 'seats', 'taken_seats'
    )
    search_fields = ('title', 'city', 'start_at', 'end_at')
    list_filter = ('title', 'city', 'start_at', 'end_at')
    ordering = ('city',)
    empty_value_display = '-пусто-'

    def taken_seats(self, obj):
        return obj.taken_seats