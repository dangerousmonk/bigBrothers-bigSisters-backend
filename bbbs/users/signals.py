from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .services import send_email

User = get_user_model()


@receiver(post_save, sender=User)
def send_email_to_new_user(sender, instance, created, **kwargs):
    if created:
        name = instance.get_full_name()
        email = instance.email
        email_subject = _('Your credentials')
        email_body = f'{instance.email} - {instance.password}'
        data = {'email_subject': email_subject, 'email_to': [email], 'email_body': email_body}
        send_email(data)
