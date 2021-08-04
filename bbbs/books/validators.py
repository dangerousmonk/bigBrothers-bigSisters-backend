import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def year_validator(value):
    if value < 1800 or value > datetime.datetime.now().year:
        raise ValidationError(
            _('%(value)s - invalid year, ask administrator for help'),
            params={'value': value},
        )
