from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class VideosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bbbs.videos'
    verbose_name = _('Videos')
