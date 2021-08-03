from rest_framework import serializers

from .models import Place



class InfoField(serializers.Field):
    def to_representation(self, place):
        display = ''
        if place.gender:
            display += place.get_gender(place.gender) + ', '
        display += str(place.age) + ' лет. '
        display += place.get_activity_type(place.activity_type) + ' отдых'
        return display


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
            'imageUrl',
            'city',
            #'tags'
        ]


class PlaceWriteSerializer(serializers.ModelSerializer):
    info = InfoField(source='*', read_only=True)
    imageUrl = serializers.ImageField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    chosen = serializers.BooleanField(read_only=True)

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
            'imageUrl',
            'city',
            #'tags'
        ]