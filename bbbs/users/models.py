from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        MODERATOR_REG = 'moderator_reg', _('Regional moderator')
        MODERATOR = 'moderator', _('Moderator')
        MENTOR = 'mentor', _('Mentor')
        CURATOR = 'curator', _('Curator')
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
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MENTOR,
        verbose_name=_('User role')
    )
    city = models.ForeignKey(
        'common.City',
        related_name='users',
        null=True,
        on_delete=models.SET_NULL,
    )
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['username']

    def __str__(self):
        return self.get_full_name()

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_moderator_reg(self):
        return self.role == self.Role.MODERATOR_REG

    @property
    def is_mentor(self):
        return self.role == self.Role.MENTOR

    @property
    def is_curator(self):
        return self.role == self.Role.CURATOR