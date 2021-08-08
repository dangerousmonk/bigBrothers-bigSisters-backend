from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class StoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bbbs.story'
    verbose_name = _('Stories')
