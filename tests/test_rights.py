from django.conf import settings
from django.urls import reverse

import pytest

from bbbs.common.choices import TagChoices

from . import factories

pytestmark = pytest.mark.django_db
PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')


def test_rights_endpoint_available(client):
    tags = factories.TagFactory.create_batch(3, model=TagChoices.RIGHTS)
    factories.RightFactory.create_batch(PAGE_SIZE + 1, tags=tags)
    url = reverse('rights-list')
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


def test_rights_detail_endpoint_avilable(client):
    tags = factories.TagFactory.create_batch(3, model=TagChoices.RIGHTS)
    right = factories.RightFactory.create(tags=tags)
    url = reverse('rights-detail', kwargs={'pk': right.id})
    expected = {
        'title': right.title,
        'description': right.description,
        'text': right.text,
        'color': right.color,
        'image': right.image,
        'tags': [{'id': tag.id, 'name': tag.name, 'slug': tag.slug} for tag in tags]
    }
    response = client.get(url)

    assert response.status_code == 200
    assert expected == response.json()


def test_right_endpoint_readonly(mentor_client):
    right = factories.RightFactory.create()
    url_list = reverse('rights-list')
    url_detail = reverse('rights-detail', kwargs={'pk': right.id})

    response = mentor_client.post(url_list, data={})
    assert response.status_code == 405

    response = mentor_client.patch(url_detail, data={})
    assert response.status_code == 405

    response = mentor_client.delete(url_detail)
    assert response.status_code == 405


def test_rights_extra_tag_action_available(client):
    tags = factories.TagFactory.create_batch(5, model=TagChoices.RIGHTS)
    url = reverse('rights-tags')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == len(tags)


OTHER_TAGS = [
    TagChoices.EVENTS,
    TagChoices.MOVIES,
    TagChoices.PLACES,
    TagChoices.QUESTIONS,
    TagChoices.BOOKS,
]


@pytest.mark.parametrize('model', OTHER_TAGS)
def test_rights_tag_action_returns_only_tags_for_rights(client, model):
    rights_tags = factories.TagFactory.create_batch(5, model=TagChoices.RIGHTS)
    factories.TagFactory.create_batch(10, model=model)
    url = reverse('rights-tags')
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == len(rights_tags)
