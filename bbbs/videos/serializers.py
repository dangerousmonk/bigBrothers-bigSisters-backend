from rest_framework import serializers

from bbbs.common.serializers import TagSerializer

from .models import Video, Movie


class VideoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    image = serializers.ImageField(
        allow_empty_file=False,
        required=False,
    )

    class Meta:
        model = Video
        fields = [
            'id',
            'added_at',
            'title',
            'description',
            'image',
            'link',
            'duration_in_seconds',
            'tags',
            'show_on_main',
        ]


class MovieSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    image = serializers.ImageField(
        allow_empty_file=False,
        required=False,
    )

    class Meta:
        model = Movie
        fields = [
            'id',
            'added_at',
            'title',
            'description',
            'annotation',
            'link',
            'tags',
            'image',
            'show_on_main',
        ]