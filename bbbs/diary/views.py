from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from requests.exceptions import RequestException
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bbbs.common.permissions import IsOwnerAdminModeratorOrReadOnly
from bbbs.users.serializers import EmailSerializer
from bbbs.users.services import send_email

from .models import Diary
from .serializers import DiarySerializer


class DiaryViewSet(viewsets.ModelViewSet):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerAdminModeratorOrReadOnly]

    def get_queryset(self):
        return Diary.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post'], detail=True)
    def send_curator(self, request, pk=None):
        author = request.user
        if not author.is_mentor:
            data = {
                'success': False,
                'message': _('only mentors can send diaries to their curators')
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        diary = get_object_or_404(Diary, pk=pk, author=author)

        if not diary.sent_to_curator:
            to_email = author.curator.email
            serializer = EmailSerializer(data={'email': to_email})
            serializer.is_valid(raise_exception=True)

            author_name = author.get_full_name()
            subject_msg = _('Added new diary from')
            email_subject = f'{author_name} - {subject_msg} {diary.meeting_date}'
            email_body = diary.description
            data = {'email_subject': email_subject, 'email_to': [to_email], 'email_body': email_body}

            try:
                send_email(data)
            except RequestException:
                data = {
                    'Success': False,
                    'message': _('Failed to send link, try again later')
                }
                return Response(data=data, status=status.HTTP_504_GATEWAY_TIMEOUT)

            diary.sent_to_curator = True
            diary.save(update_fields=['sent_to_curator'])
            data = {
                'Success': True,
                'message': _('Sent diary to your curator')
            }
            return Response(data=data, status=status.HTTP_200_OK)

        data = {
            'Success': False,
            'message': _('You have already sent this diary to curator')
        }
        return Response(data=data, status=status.HTTP_200_OK)
