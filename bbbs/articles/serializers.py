from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=False,
        allow_empty_file=False,
        use_url=False,
    )

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'author_info',
            'article_url',
            'content',
            'image',
        ]