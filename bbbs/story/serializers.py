from rest_framework import serializers

from .models import Story

from bbbs.users.serializers import AuthorSerializer


class StorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=False, use_url=False, required=False)
    author = serializers.EmailField(read_only=True, source='author.email')

    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'child_name',
            'friends_since',
            'author',
            'added_at',
            'intro',
            'text',
            'quote',
            'image',
        ]
