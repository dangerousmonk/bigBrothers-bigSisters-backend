from .serializers import ProfileSerializer, EmailSerializer, SetNewPasswordSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from django.conf import settings
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import permissions
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import CustomUser


class ProfileViewSet(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response({'OK': 'Link has been sent for password reset'}, status=status.HTTP_200_OK)


class PasswordResetCheck(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(settings.AUTH_USER_MODEL, id=id)
            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                return Response({'Invalid Token': 'Token is invalid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({'Success': True, 'message': 'Credentials valid', 'uidb64': uidb64})
        except DjangoUnicodeDecodeError:
            return Response({'Invalid Token': 'Token is invalid, please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data={'success': True, 'message': 'Password changed'}, status=status.HTTP_200_OK)
