from django.db import models
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    title = models.CharField(
        max_length=180,
        verbose_name=_('title'),
    )
    author_info = models.CharField(
        max_length=180,
        verbose_name=_('author information'),
    )
    article_url = models.URLField(
        max_length=180,
        verbose_name=_('link to article'),
    )
    content = models.TextField(
        verbose_name=_('content'),
    )
    image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name=_('image'), # TODO: validate image size,
    )
    show_on_main = models.BooleanField(
        default=False,
        verbose_name=_('show on main page'),
        help_text=_('choose to display on the home page')
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_('added at'))

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-added_at']

    def __str__(self):
        return self.title
