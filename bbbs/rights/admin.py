from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from bbbs.common.models import Tag

from .models import Right


@admin.register(Right)
class RightAdmin(ModelAdmin):
    list_display = ('id', 'title', 'get_description')
    search_fields = ('title', 'description', 'text')
    list_filter = ('tags','color',)

    @admin.display(description=_('description'))
    def get_description(self, obj):
        description = obj.description
        if description is not None:
            return f'{description[:30]}...'
        return description

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            kwargs['queryset'] = Tag.objects.filter(model='rights')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

