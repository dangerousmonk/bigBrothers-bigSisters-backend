from django.conf import settings
from django.urls import reverse

import pytest

from bbbs.common.choices import TagChoices

from . import factories

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


def test_books_extra_tag_action_available(client):
    tags = factories.TagFactory.create_batch(5, model=TagChoices.BOOKS)
    url = reverse('books-tags')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == len(tags)


OTHER_TAGS = [
    TagChoices.EVENTS,
    TagChoices.MOVIES,
    TagChoices.PLACES,
    TagChoices.QUESTIONS,
    TagChoices.RIGHTS,
]


@pytest.mark.parametrize('model', OTHER_TAGS)
def test_books_tag_action_returns_only_tags_for_books(client, model):
    books_tags = factories.TagFactory.create_batch(5, model=TagChoices.BOOKS)
    factories.TagFactory.create_batch(10, model=model)
    url = reverse('books-tags')
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == len(books_tags)
