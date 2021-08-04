from django.contrib import admin
from .models import Book
from bbbs.common.models import Tag
from django.contrib.admin import ModelAdmin, register
from django.contrib import admin
from django.utils.translation import gettext_lazy as _




@register(Book)
class PlaceAdmin(ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'year', 'description', 'color',
        'url', 'slug', 'added_at', 'get_tags',
    )
    readonly_fields = []
    #search_fields = ('title', 'city', 'tags')
    #list_filter = ('chosen', 'showOnMain', 'activity_type', 'age', 'tags')
    #empty_value_display = '-пусто-'
    #ordering = ('chosen', '-pubDate')

    @admin.display(description=_('tags'))
    def get_tags(self, obj):
        qs = obj.list_tags()
        if qs:
            return list(qs)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_moderator_reg:
            return queryset.filter(city=request.user.city)
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        form = super(PlaceAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_moderator_reg:
            form.base_fields['city'].initial = request.user.city
            form.base_fields['city'].disabled = True
            form.base_fields['city'].help_text = _('Can only add in your own city')
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            kwargs['queryset'] = Tag.objects.filter(model='books')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

