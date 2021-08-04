from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import year_validator
from bbbs.utils import unique_slugify


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
        verbose_name=_('publication date'),
        validators=[year_validator, ],
    )
    description = models.TextField(
        max_length=1024,
        verbose_name=_('description'),
    )
    color = models.CharField(
        max_length=7,
        default='#E26C2D',  # TODO: change default, add default choices
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
    added_at = models.DateTimeField(auto_now_add=True)
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

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = unique_slugify(self.title, self.__class__)
        return super().save(*args, **kwargs)

    def list_tags(self):
        return self.tags.values_list('name', flat=True)
