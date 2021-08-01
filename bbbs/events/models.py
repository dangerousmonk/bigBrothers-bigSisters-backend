from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    address = models.CharField(max_length=200, verbose_name=_('address'))
    contact = models.CharField(max_length=200, verbose_name=_('contact'))
    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
        unqiue=True,
    )
    description = models.TextField(verbose_name=_('description'))
    start_at = models.DateTimeField(verbose_name=_('date start'))
    end_at = models.DateTimeField(verbose_name=_('date finish'))
    seats = models.PositiveSmallIntegerField(verbose_name='seats number')
    city = models.ForeignKey(
        'common.City',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('city'),
        related_name='events',
    )

    # TODO: need Tag?

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-start_at', 'city']
        constraints = [
            models.UniqueConstraint(
                fields=['city', 'title'],
                name='unique-event')
        ]

    def __str__(self):
        return self.title  # TODO: not only title
