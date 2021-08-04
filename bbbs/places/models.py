from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator




class Place(models.Model):
    class Genders(models.TextChoices):
        MALE = 'M', _('Мальчик')
        FEMALE = 'F', _('Девочка')

    class ActivityTypes(models.IntegerChoices):
        ACTIVE = 0, _('Активный')
        ENTERTAINING = 1, _('Развлекательный')
        INFORMATIVE = 2, _('Познавательный')

    chosen = models.BooleanField(
        default=False,
        verbose_name=_('Выбор наставника'),
    )
    verified = models.BooleanField(
        default=False,
        verbose_name=_('Проверено для публикации'),
    )
    show_on_main = models.BooleanField(
        default=True,
        verbose_name=_('Показать на главной'),
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название'),
    )
    address = models.CharField(
        max_length=200,
        verbose_name=_('Адрес'),
    )
    city = models.ForeignKey(
        'common.City',
        related_name='places',
        on_delete=models.CASCADE,
        verbose_name=_('city'),
    )
    gender = models.CharField(
        choices=Genders.choices,
        max_length=1,
        null=True,
        blank=True,
        verbose_name=_('gender'),
    )
    age = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(18)],
        verbose_name=_('age'),
    )
    activity_type = models.PositiveSmallIntegerField(
        choices=ActivityTypes.choices,
        verbose_name=_('activity type'),
    )
    description = models.TextField(
        verbose_name=_('Комментарий'),
        help_text=_('share your experience'),
    )
    link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('link'),
        help_text=_('link to the website'),
    )
    tags = models.ManyToManyField(
        'common.Tag',
        related_name='places',
        blank=True,
        verbose_name=_('Теги')
    )
    image_url = models.ImageField(
        null=True,
        blank=True,
        upload_to='places/',
        verbose_name=_('image'),
        help_text=_('add image'),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('publication date')
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = _('Place - where to go?')
        verbose_name_plural = _('Places - where to go?')

    def __str__(self):
        return self.title

    def list_tags(self):
        return self.tags.values_list('name', flat=True)

    def get_gender(self, gender_code):
        return self.Genders(gender_code).label

    def get_activity_type(self, type_code):
        return self.ActivityTypes(type_code).label