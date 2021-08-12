import pytest
from django.urls import reverse
from django.conf import settings
from . import factories
from bbbs.common.choices import TagChoices

pytestmark = pytest.mark.django_db
PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')


def test_book_list_endpoint_available(client):
    tags = factories.TagFactory.create_batch(5, model=TagChoices.BOOKS)
    factories.BookFactory.create_batch(PAGE_SIZE + 1, tags=tags)
    url = reverse('books-list')
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


def test_book_detail_endpoint_available(client):
    tags = factories.TagFactory.create_batch(3, model=TagChoices.BOOKS)
    book = factories.BookFactory.create(tags=tags)
    url = reverse('books-detail', kwargs={'pk': book.id})
    expected = {
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'description': book.description,
        'color': book.color,
        'url': book.url,
        'slug': '',  # TODO: remove slug
        'tags': [{'id': tag.id, 'name': tag.name, 'slug': tag.slug} for tag in tags]
    }
    response = client.get(url)

    assert response.status_code == 200
    assert expected == response.json()


def test_books_endpoint_read_only(mentor_client):
    book = factories.BookFactory.create()
    url_list = reverse('books-list')
    url_detail = reverse('books-detail', kwargs={'pk': book.id})

    response = mentor_client.post(url_list, data={})
    assert response.status_code == 405

    response = mentor_client.patch(url_detail, data={})
    assert response.status_code == 405

    response = mentor_client.delete(url_detail)
    assert response.status_code == 405
