from rest_framework import serializers

from .models import Book
from bbbs.common.serializers import TagSerializer

class BookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'year',
            'description',
            'color',
            'url',
            'slug',
            'tags',

        ]