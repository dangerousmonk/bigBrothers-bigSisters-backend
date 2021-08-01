from django.core.exceptions import ValidationError
from django.utils import timezone as tz


def validate_date_not_in_future(value):
    if value > tz.now():
        raise ValidationError('date is in the future')
