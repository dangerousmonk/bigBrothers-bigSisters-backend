from django.db import models
from django.utils.translation import gettext_lazy as _

from bbbs.common.choices import RightColorChoices


class Right(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('title')
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_('description')
    )
    text = models.TextField(
        verbose_name=_('text')
    )
    color = models.CharField(
        max_length=7,
        choices=RightColorChoices.CHOICES,  # TODO: help text ?
        verbose_name=_('color'),
    )
    image = models.ImageField(
        upload_to='rights/',
        blank=True,
        null=True,
        verbose_name=_('image'),  # TODO: validate image size
    )
    tags = models.ManyToManyField(
        'common.Tag',
        related_name='rights',
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

    def __str__(self):
        return self.title