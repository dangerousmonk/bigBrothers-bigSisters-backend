from django.contrib import admin
from django.contrib.admin import ModelAdmin, register, site

from bbbs.common.models import Tag

from .models import Event, EventParticipant

admin.site.register(EventParticipant)

@register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('city', 'title', 'start_at', 'end_at', 'seats', 'taken_seats')
    search_fields = ('title', 'city', 'start_at', 'end_at')
    list_filter = ('title', 'city', 'start_at', 'end_at')
    ordering = ('city',)
    empty_value_display = '-пусто-'

    def taken_seats(self, obj):
        return obj.taken_seats


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = Event.event_objects.with_taken_seats()
        if request.user.is_moderator_reg:
            return queryset.filter(city=request.user.city)
        return queryset

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            kwargs['queryset'] = Tag.objects.filter(model='events')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def has_module_permission(self, request):
        return not request.user.is_anonymous

    def has_view_permission(self, request, obj=None):
        return not request.user.is_anonymous

    def has_add_permission(self, request):
        return not request.user.is_anonymous

    def has_change_permission(self, request, obj=None):
        return not request.user.is_anonymous

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_anonymous

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_moderator_reg:
            form.base_fields['city'].initial = request.user.city
            form.base_fields['city'].disabled = True
            form.base_fields['city'].help_text = 'Вы можете добавить событие только в своем городе'
        return form

