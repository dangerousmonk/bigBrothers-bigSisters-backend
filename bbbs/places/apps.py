from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bbbs.places'
    verbose_name = _('Places')
