from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bbbs.articles'
    verbose_name = _('Articles')
