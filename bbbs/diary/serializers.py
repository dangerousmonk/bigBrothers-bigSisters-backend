from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import gettext_lazy as _

from .models import Diary
from datetime import date


class DiarySerializer(serializers.ModelSerializer):
    sent_to_curator = serializers.BooleanField(read_only=True)
    place = serializers.CharField(min_length=2, max_length=100)
    image = serializers.ImageField(allow_empty_file=False, use_url=False, required=False, )
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_meeting_date(self, value):
        today = date.today()
        if value > today or value.year < 2021:
            raise serializers.ValidationError(
                _('Date can not be in the future or earlier 2021')
            )
        return value

    class Meta:
        model = Diary
        fields = [
            'id',
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
                fields=['author', 'place', 'meeting_date'],
                message=_('You have already wrote a diary with this place and date'),
            )
        ]
