from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Story(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name=_('title'),
        unique=True,
    )
    child_name = models.CharField(
        max_length=70,
        verbose_name=_('child name'),
    )
    friends_since = models.DateTimeField(  # TODO: validation
        verbose_name=_('friends since'),
    )
    show_on_main = models.BooleanField(
        default=False,
        verbose_name=_('show on main page'),
        help_text=_('choose to display on the home page')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stories',
        verbose_name=_('story author'),

    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('story added at'),
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('story modified at'),
    )
    intro = models.CharField(
        max_length=200,
        verbose_name=_('story intro'),
    )
    text = models.TextField(
        verbose_name=_('story text'),
    )
    quote = models.CharField(
        max_length=150,
        verbose_name=_('quote'),
    )
    image = models.ImageField(
        upload_to='stories/',
        blank=True,
        null=True,
        verbose_name=_('image'),
    )

    class Meta:
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')
        ordering = ['-added_at']

    def __str__(self):
        return self.title
