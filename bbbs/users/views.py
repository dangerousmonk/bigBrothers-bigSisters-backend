from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import ProfileReadSerializer, ProfileWriteSerializer


class ProfileAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ProfileWriteSerializer
        return ProfileReadSerializer

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ProfileWriteSerializer(
            instance=user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = ProfileReadSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)