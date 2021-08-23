from django.conf import settings
from django.urls import reverse

import pytest

from . import factories

pytestmark = pytest.mark.django_db
PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')


def test_articles_endpoint_available(client):
    factories.ArticleFactory.create_batch(PAGE_SIZE + 1)
    url = reverse('articles-list')
    response = client.get(url)
    response_data = response.json()

    assert response.status_code == 200
    assert 'count' in response_data
    assert 'next' in response_data
    assert 'previous' in response_data
    assert 'results' in response_data
    assert type(response_data['results']) == list
    assert response_data['count'] == PAGE_SIZE + 1
    assert len(response_data['results']) == PAGE_SIZE


def test_articles_detail_endpoint_avilable(client):
    article = factories.ArticleFactory.create()
    url = reverse('articles-detail', kwargs={'pk': article.id})
    expected = {
        'id': article.id,
        'title': article.title,
        'author_info': article.author_info,
        'article_url': article.article_url,
        'content': article.content,
        'image': article.image,
    }
    response = client.get(url)

    assert response.status_code == 200
    assert expected == response.json()


def test_article_endpoint_readonly(mentor_client):
    article = factories.ArticleFactory.create()
    url_list = reverse('articles-list')
    url_detail = reverse('articles-detail', kwargs={'pk': article.id})

    response = mentor_client.post(url_list, data={})
    assert response.status_code == 405

    response = mentor_client.patch(url_detail, data={})
    assert response.status_code == 405

    response = mentor_client.delete(url_detail)
    assert response.status_code == 405
