from rest_framework import serializers

from bbbs.common.serializers import TagSerializer

from .models import Right


class RightSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=False,
        allow_empty_file=False,
        use_url=False,
    )
    tags = TagSerializer(many=True, read_only=True)
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