import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def year_validator(value):
    if value < 1800 or value > datetime.datetime.now().year:
        raise ValidationError(
            _('%(value)s - invalid year, enter the sensible year value'),
            params={'value': value},
        )


def diary_year_validator(value):
    if value.year < 2021 or value > datetime.date.today():
        raise ValidationError(
            _('%(value)s - invalid date, can not be in the future or earlier last year'),
            params={'value': value},
        )
