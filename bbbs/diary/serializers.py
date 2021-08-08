from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import gettext_lazy as _

from .models import Diary


class DiarySerializer(serializers.ModelSerializer):
    sent_to_curator = serializers.BooleanField(read_only=True)
    place = serializers.CharField(min_length=2, max_length=100)
    image = serializers.ImageField(allow_empty_file=False, use_url=False, required=False, )
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Diary
        fields = [
            'place',
            'meeting_date',
            'added_at',
            'modified_at',
            'description',
            'image',
            'sent_to_curator',
            'mark',
            'author',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Diary.objects.all(),
                fields=['author', 'place', 'date'],
                message=_('You have already wrote a diary with this place and date'),
            )
        ]
