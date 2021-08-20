from django.conf import settings
from django.urls import reverse

import pytest

from bbbs.common.choices import TagChoices

from . import factories

pytestmark = pytest.mark.django_db
PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')


def test_events_unavailable_for_unauthorized(client):
    url = reverse('events-list')
    response = client.get(url)
    assert response.status_code == 401


def test_events_available_for_authorized(mentor, mentor_client):
    tags = factories.TagFactory.create_batch(5, model=TagChoices.EVENTS)
    factories.EventFactory.create_batch(PAGE_SIZE + 1, tags=tags, city=mentor.city)
    url = reverse('events-list')
    response = mentor_client.get(url)
    response_data = response.json()

    assert response.status_code == 200
    assert 'count' in response_data
    assert 'next' in response_data
    assert 'previous' in response_data
    assert 'results' in response_data
    assert type(response_data['results']) == list
    assert response_data['count'] == PAGE_SIZE + 1
    assert len(response_data['results']) == PAGE_SIZE


def test_events_detail_endpoint_available(mentor_client):
    pass


def test_events_endpoint_read_only(mentor_client):
    event = factories.EventFactory.create()
    url_list = reverse('events-list')
    url_detail = reverse('books-detail', kwargs={'pk': event.id})

    response = mentor_client.post(url_list, data={})
    assert response.status_code == 405

    response = mentor_client.patch(url_detail, data={})
    assert response.status_code == 405

    response = mentor_client.delete(url_detail)
    assert response.status_code == 405


def test_events_extra_tag_action_available(mentor_client):
    tags = factories.TagFactory.create_batch(5, model=TagChoices.EVENTS)
    url = reverse('events-tags')
    response = mentor_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == len(tags)
