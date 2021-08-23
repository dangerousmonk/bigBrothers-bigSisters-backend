from rest_framework import serializers

from bbbs.common.serializers import TagSerializer

from .fields import InfoField
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    info = InfoField(source='*', read_only=True)
    image = serializers.ImageField(
        required=False,
        allow_empty_file=False,
        use_url=False,
    )
    chosen = serializers.BooleanField(read_only=True)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Place
        fields = [
            'id',
            'info',
            'chosen',
            'activity_type',
            'age',
            'gender',
            'title',
            'address',
            'description',
            'link',
            'image_url',
            'tags'
        ]