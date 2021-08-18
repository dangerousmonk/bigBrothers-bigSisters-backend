from django.contrib.auth import get_user_model
from rest_framework import serializers
from bbbs.common.serializers import CitySerializer

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


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, min_length=2)

    class Meta:
        fields = ['email']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]
