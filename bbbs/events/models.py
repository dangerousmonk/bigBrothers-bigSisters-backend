from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, Exists, OuterRef
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from bbbs.common.validators import event_seats_validator


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

    def with_finished_for_user(self, user, city):
        """
        Return only events in users city that have ended
        :param user: User instance
        :param city: City instance
        :return: Event queryset
        """
        qs = self.with_booked(user=user)
        qs = qs.with_taken_seats()
        return qs.filter(city=city, end_at__lt=now())

    def with_not_finished_for_guest(self, city):
        """
        Return only events in query_params city that haven't ended
        :param city: City instance
        :return: Event queryset
        """
        qs = self.with_taken_seats()
        return qs.filter(city=city, end_at__gt=now()) #TODO: events only for authorized


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
    tags = models.ManyToManyField(
        'common.Tag',
        related_name='events',
        verbose_name=_('tags'),
        blank=True,
        help_text=_('tags appropriate for this event'),
    )
    objects = models.Manager()
    event_objects = EventsQuerySet.as_manager()

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
        return self.title

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

    def list_tags(self):
        return self.tags.values_list('name', flat=True)


class EventParticipantQuerySet(models.QuerySet):
    def not_finished_for_user(self, user):
        """
        Return only users registrations that haven't ended
        :param user: User instance
        :return: EventParticipant queryset
        """
        return self.select_related('event').filter(
            user=user, event__end_at__gt=now()
        )


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
        validators=[event_seats_validator],
        verbose_name=_('event'),
    )
    registered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('registration date'),
    )
    objects = models.Manager()
    participants_objects = EventParticipantQuerySet.as_manager()

    class Meta:
        verbose_name = _('Event participant')
        verbose_name_plural = _('Event participants')
        ordering = ['event__start_at', '-registered_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'], name='unique-participant'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'
