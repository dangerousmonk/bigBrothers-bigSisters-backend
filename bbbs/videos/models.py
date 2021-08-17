from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Video(models.Model):
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('added_at')
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=200,
    )
    description = models.CharField(
        verbose_name=_('description'),
        max_length=250,
    )
    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='videos/',
        blank=True,
        null=True,
    )
    link = models.URLField(
        verbose_name=_('link to video'),
        max_length=200,
        unique=True,
    )
    duration_in_seconds = models.PositiveSmallIntegerField(
        verbose_name=_('video duration in seconds'),
        validators=(MinValueValidator(1), MaxValueValidator(36000)),
    )
    tags = models.ManyToManyField(
        'common.Tag',
        verbose_name=_('tags'),
        related_name='videos',
    )
    show_on_main = models.BooleanField(
        verbose_name=_('show on main page'),
        default=False,
        help_text=_('choose to display on the main page'),
    )

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
        ordering = ['-added_at', ]

    def __str__(self):
        return self.title
