from rest_framework import serializers

from .models import City, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name',
            'slug',
        ]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'id',
            'name',
            'is_primary',
        ]
