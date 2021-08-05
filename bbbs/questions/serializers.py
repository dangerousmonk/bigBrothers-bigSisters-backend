from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    answer = serializers.CharField(read_only=True)
    added_at = serializers.DateTimeField(read_only=True)
    show_on_main = serializers.BooleanField(read_only=True)


    class Meta:
        model = Question
        fields = [
            'id',
            'question',
            'answer',
            'added_at',
            'show_on_main',
            'tags',         # TODO: make nested
        ]

