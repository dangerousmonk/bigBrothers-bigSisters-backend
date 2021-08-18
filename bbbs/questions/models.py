from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    question = models.CharField(
        max_length=255,
        verbose_name=_('question'),
    )
    answer = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('answer'),
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('publication date'),
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('modified at'),
    )
    show_on_main = models.BooleanField(
        default=False,
        verbose_name=_('show on main page'),
        help_text=_('choose to display on the home page')
    )
    tags = models.ManyToManyField(
        'common.Tag',
        related_name='questions',
        blank=True,
        verbose_name=_('questions'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('author'),

    )

    class Meta:
        ordering = ['-added_at']
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.question[:30]

    def list_tags(self):
        return self.tags.values_list('name')
