from django.utils.translation import gettext_lazy as _
from django.contrib.admin import ModelAdmin, register, site

from bbbs.common.models import Tag

from .models import Place


@register(Place)
class EventAdmin(ModelAdmin):
    list_display = ('id', 'title', 'address', 'city',
                    'gender', 'age', 'activity_type',
                    'pub_date', 'author',
                    'chosen', 'verified', 'show_on_main'
                    )
    search_fields = ('title', 'address',)
    list_filter = ('city', 'gender', 'age', 'activity_type', 'author', 'chosen', 'verified', 'show_on_main')
    ordering = ('-pub_date',)
    empty_value_display = _('-empty-')


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = Place.objects.all()
        if request.user.is_moderator_reg:
            return queryset.filter(city=request.user.city)
        return queryset

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            kwargs['queryset'] = Tag.objects.filter(model='places')
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
            form.base_fields['city'].help_text = _('You can add place only in your city')
        return form

