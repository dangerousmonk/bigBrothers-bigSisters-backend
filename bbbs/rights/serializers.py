from rest_framework import serializers

from .models import Right


class RightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Right
        fields = [
            'title',
            'description',
            'text',
            'color',
            'image',
            'tags',
        ]