from django.db import models
from django.utils.translation import gettext_lazy as _

from bbbs.common.choices import BookColorChoices

from .validators import year_validator


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
    )
    author = models.CharField(
        max_length=200,
        verbose_name=_('author'),
    )
    year = models.PositiveSmallIntegerField(
        verbose_name=_('publication year'),
        validators=[year_validator, ],
    )
    description = models.TextField(
        max_length=1024,
        verbose_name=_('description'),
    )
    color = models.CharField(
        max_length=7,
        choices=BookColorChoices.CHOICES,  # TODO: help text ?
        verbose_name=_('color'),
    )
    url = models.URLField(
        verbose_name=_('book url')
    )
    slug = models.SlugField(
        max_length=200,
        editable=False,
        verbose_name=_('slug'),
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_('added_at'))
    tags = models.ManyToManyField(
        'common.Tag',
        related_name='books',
        verbose_name=_('tags')
    )

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        ordering = ['-added_at', ]

    def __str__(self):
        return self.title

    def list_tags(self):
        return self.tags.values_list('name', flat=True)
