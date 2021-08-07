from rest_framework import serializers

from .models import Story


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'child_name',
            'friends_since',
            'show_on_main',
            'author',
            'story_added_at',
            'intro',
            'text',
            'quote',
            'image',
        ]
        read_only_fields = ['show_on_main', 'author', 'story_added_at']
