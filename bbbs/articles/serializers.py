from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta:
        model = Article
        exclude = ['image_url']