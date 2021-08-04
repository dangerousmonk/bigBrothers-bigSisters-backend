from django.contrib.auth import get_user_model
from django.db import models
from django.core import validators
from django.db.models import Count, OuterRef, Exists
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class EventsQuerySet(models.QuerySet):

    def with_booked(self, user):
        sub_qs = EventParticipant.objects.filter(
            user=user, event=OuterRef('id')
        )
        return self.annotate(booked=Exists(sub_qs))

    def with_taken_seats(self):
        return self.annotate(taken_seats=Count('participants'))

    def with_not_finished_for_user(self, user, city):
        """
        Return only events in users city that haven't ended
        :param user: User instance
        :param city: City instance
        :return: Event queryset
        """
        qs = self.with_booked(user=user)
        qs = qs.with_taken_seats()
        return qs.filter(city=city, end_at__gt=now())

    def with_not_finished_for_guest(self, city):
        """
        Return only events in query_params city that haven't ended
        :param city: City instance
        :return: Event queryset
        """
        qs = self.with_taken_seats()
        return qs.filter(city=city, end_at__gt=now())


class Event(models.Model):
    address = models.CharField(max_length=200, verbose_name=_('address'))
    contact = models.CharField(max_length=200, verbose_name=_('contact'))
    title = models.CharField(
        max_length=200,
        verbose_name=_('title'),
        unique=True,
    )
    description = models.TextField(verbose_name=_('description'))
    start_at = models.DateTimeField(verbose_name=_('date start'))
    end_at = models.DateTimeField(verbose_name=_('date finish'))
    seats = models.PositiveSmallIntegerField(
        verbose_name='seats number',
        validators=[validators.MinValueValidator(1)],
    )
    city = models.ForeignKey(
        'common.City',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('city'),
        related_name='events',
    )
    objects = models.Manager()
    event_objects = EventsQuerySet.as_manager()

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

    def clean(self):

        if self.start_at >= self.end_at:
            raise ValidationError(
                {'start_at': _('Start date can not be later or equal the end date')}
            )

        if self.start_at < now():
            raise ValidationError(
                {'start_at': _('Start date can not be the past date')}
            )

        if self.end_at < now():
            raise ValidationError(
                {'end_at': _('End date can not be the past date')}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class EventParticipant(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='participations',
        verbose_name=_('event participant'),
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='participants',
        verbose_name=_('event'),
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)  # TODO: is this needed?

    class Meta:
        verbose_name = _('Event participant')
        verbose_name_plural = _('Event participants')
        ordering = ['event', '-registered_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'], name='unique-participant'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'
