from rest_framework import serializers

from bbbs.common.serializers import TagSerializer

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,read_only=True)

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'year',
            'description',
            'color',
            'url',
            'tags',
        ]
