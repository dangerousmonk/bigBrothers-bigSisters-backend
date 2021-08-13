from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core import exceptions as django_exceptions
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.timezone import now

from requests.exceptions import RequestException
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from bbbs.common.serializers import CitySerializer

from .services import send_email

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'city',
        ]


class BaseEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, min_length=2)

    class Meta:
        fields = ['email']


class EmailSerializer(BaseEmailSerializer):
    email = serializers.EmailField(required=True, min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            email = attrs['data'].get('email', '')
            if User.objects.filter(email=email).exists():
                user = settings.AUTH_USER_MODEL.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user)
                current_domain = get_current_site(request=attrs['data'].get('request')).domain
                relative_link = reverse('password-reset-check', kwargs={'uidb64': uidb64, 'token': token})
                absolute_url = 'http://' + current_domain + relative_link
                email_body = f'Hello \n you request password change at {current_domain}. Use link to reset your password \n {absolute_url}'
                data = {'email_subject': 'Reset your password', 'email_to': [user.email], 'email_body': email_body}
                send_email(data)
                return attrs
            return Response(data={'Success': False, 'message': 'No user found with provivded email'},
                            status=status.HTTP_404_NOT_FOUND)
        except RequestException:
            return Response(data={'Success': False, 'message': 'Failed to send link, try again later'},
                            status=status.HTTP_504_GATEWAY_TIMEOUT)


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6, max_length=86, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)  # TODO: or 404?
        try:
            validate_password(attrs['new_password'], user)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError({'Invalid': 'The reset link is invalid'}, code=401)
            user.set_password(new_password)
            if hasattr(user, 'last_login'):
                user.last_login = now()
            user.save()
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return super().validate(attrs)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]
