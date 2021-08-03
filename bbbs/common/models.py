from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import TagChoices

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


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    model = models.CharField(
        max_length=50,
        choices=TagChoices.CHOICES,
        verbose_name=_('tag model label'),
    )

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ['model']

    def __str__(self):
        return self.name