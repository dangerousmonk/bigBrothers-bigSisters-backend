from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DiaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bbbs.diary'
    verbose_name = _('Diaries')
