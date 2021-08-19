from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from bbbs.common.mixins import TagAdminMixin

from .models import Movie, Video


@admin.register(Video)
class VideoAdmin(TagAdminMixin):
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


@admin.register(Movie)
class MovieAdmin(TagAdminMixin):
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