import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def year_validator(value):
    if value == 0 or value > datetime.datetime.now().year:  # TODO: funny years like 123 should be possible?
        raise ValidationError(
            _('%(value)s - year can not be in the future or equals zero'),
            params={'value': value},
        )
