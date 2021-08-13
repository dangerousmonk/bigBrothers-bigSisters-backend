import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def year_validator(value):
    if value > datetime.date.today():
        raise ValidationError(
            _('%(value)s - invalid date, can not be in the future'),
            params={'value': value},
        )