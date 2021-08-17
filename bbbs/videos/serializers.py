from rest_framework import serializers

from bbbs.common.serializers import TagSerializer

from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    image = serializers.ImageField(
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'description',
            'image',
            'link',
            'duration',
            'show_on_main',
            'tags',
            'added_at',
        ]