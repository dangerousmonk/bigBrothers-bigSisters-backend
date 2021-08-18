from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from bbbs.common.models import Tag

from .models import Video, Movie


@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = ('id', 'added_at', 'title',
                    'get_description', 'duration_in_seconds', 'get_tags',
                    'show_on_main', 'link', 'image')
    search_fields = ('title', 'description', 'text')
    list_filter = ('tags','show_on_main',)

    @admin.display(description=_('description'))
    def get_description(self, obj):
        description = obj.description
        if description is not None:
            return f'{description[:30]}...'
        return description

    @admin.display(description=_('tags'))
    def get_tags(self, obj):
        qs = obj.list_tags()
        if qs:
            return list(qs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            kwargs['queryset'] = Tag.objects.filter(model='videos')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    list_display = ('id', 'added_at', 'title',
                    'get_description', 'annotation', 'get_tags',
                    'show_on_main', 'link', 'image')
    search_fields = ('title', 'description', 'text')
    list_filter = ('tags','show_on_main',)

    @admin.display(description=_('description'))
    def get_description(self, obj):
        description = obj.description
        if description is not None:
            return f'{description[:30]}...'
        return description

    @admin.display(description=_('tags'))
    def get_tags(self, obj):
        qs = obj.list_tags()
        if qs:
            return list(qs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tags':
            kwargs['queryset'] = Tag.objects.filter(model='movies')
        return super().formfield_for_manytomany(db_field, request, **kwargs)