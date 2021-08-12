from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from bbbs.common.choices import UserGenderChoices, UserRoleChoices


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_('email address')
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_('first name')
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_('last name'),
    )
    gender = models.CharField(
        max_length=1,
        choices=UserGenderChoices.CHOICES,
        verbose_name=_('user gender')
    )
    role = models.CharField(
        max_length=30,
        choices=UserRoleChoices.CHOICES,
        default=UserRoleChoices.MENTOR,
        verbose_name=_('user role')
    )
    city = models.ForeignKey(
        'common.City',
        related_name='users',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    curator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='mentors',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('curator'),
        help_text=_('choose curator if new user is mentor'),
    )
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['username']

    def __str__(self):
        return self.get_full_name()

    def clean(self):

        if self.curator and not self.is_mentor:
            raise ValidationError(
                {'curator': _('Curator can be assigned only for mentors')}
            )

        if self.is_mentor and not self.curator and not self.is_superuser:
            raise ValidationError(
                {'curator': _('Curator must be assigned to mentor')}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == UserRoleChoices.ADMIN  # TODO: or superuser when created via console

    @property
    def is_moderator(self):
        return self.role == UserRoleChoices.MODERATOR

    @property
    def is_moderator_reg(self):
        return self.role == UserRoleChoices.MODERATOR_REG

    @property
    def is_mentor(self):
        return self.role == UserRoleChoices.MENTOR

    @property
    def is_curator(self):
        return self.role == UserRoleChoices.CURATOR
