from rest_framework import serializers

from bbbs.common.serializers import TagSerializer

from .models import Place
from .fields import InfoField

class PlaceReadSerializer(serializers.ModelSerializer):
    info = InfoField(source='*')
    #tags = TagSerializer(many=True)

    class Meta:
        model = Place
        fields = [
            'id',
            'info',
            'chosen',
            'title',
            'address',
            'description',
            'link',
            'image_url',
            'city',
            #'tags'
        ]


class PlaceWriteSerializer(serializers.ModelSerializer):
    info = InfoField(source='*', read_only=True)
    image_url = serializers.ImageField(read_only=True)
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