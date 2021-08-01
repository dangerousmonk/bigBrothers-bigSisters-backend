from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class City(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name=_('city'),
        unique=True,
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_('primary City'),
    )

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ['is_primary']

    def __str__(self):
        return self.name
