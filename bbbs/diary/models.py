from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from bbbs.common.choices import DiaryMarkChoices
from bbbs.books.validators import diary_year_validator

class Diary(models.Model):
    place = models.CharField(
        verbose_name=_('place'),
        max_length=100,
        help_text=_('Meeting place')
    )
    meeting_date = models.DateField(
        verbose_name=_('meeting date'),
        validators=[diary_year_validator,],
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_('added at'))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('modified at'))
    description = models.TextField(
        verbose_name=_('description'),
        help_text=_('Describe your experience, what you liked/disliked')
    )
    image = models.ImageField(
        upload_to='diaries/',
        blank=True,
        null=True,
        verbose_name=_('image'),
    )
    sent_to_curator = models.BooleanField(
        default=False,
        verbose_name=_('sent to curator'),
        help_text=_('Shows if diary has been sent to curator'),
    )
    mark = models.CharField(
        max_length=20,
        choices=DiaryMarkChoices.CHOICES,
        verbose_name=_('mark'),
        help_text=_('Rate the time spent')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diaries',
        verbose_name=_('diary author'),
    )

    class Meta:
        verbose_name = _('Diary')
        verbose_name_plural = _('Diaries')
        ordering = ['-meeting_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'place',  'meeting_date',], name='unique-author-place-date'
            )
        ]

    def __str__(self):
        return self.place
