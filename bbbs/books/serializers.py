from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
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