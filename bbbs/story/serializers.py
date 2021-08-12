from rest_framework import serializers

from .models import Story


class StorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=False, use_url=False, required=False)

    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'child_name',
            'friends_since',
            'author',
            'story_added_at',
            'intro',
            'text',
            'quote',
            'image',
        ]
        read_only_fields = ['author', 'story_added_at']
