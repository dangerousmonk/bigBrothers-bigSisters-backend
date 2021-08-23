import time
from datetime import datetime, timedelta

from django.conf import settings
from django.urls import reverse

import pytest
import pytz

from bbbs.common.choices import TagChoices
from bbbs.events.models import EventParticipant

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


def test_events_detail_endpoint_avilable(mentor, mentor_client):
    tags = factories.TagFactory.create_batch(3, model=TagChoices.EVENTS)
    event = factories.EventFactory.create(tags=tags, city=mentor.city)
    url = reverse('events-detail', kwargs={'pk': event.id})
    is_booked = EventParticipant.objects.filter(user=mentor, event=event).exists()
    expected = {
        'id': event.id,
        'address': event.address,
        'contact': event.contact,
        'title': event.title,
        'description': event.description,
        'start_at': event.start_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'end_at': event.end_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'taken_seats': event.participants.count(),
        'booked': is_booked,
        'tags': [{'id': tag.id, 'name': tag.name, 'slug': tag.slug} for tag in tags]
    }
    response = mentor_client.get(url)
    assert response.status_code == 200
    assert expected == response.json()


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


def test_events_extra_months_action_available(mentor, mentor_client):
    event_september = factories.EventFactory.create(
        city=mentor.city,
        start_at=datetime(2022, 9, 1, 12, 0, 0, tzinfo=pytz.UTC)
    )
    event_october = factories.EventFactory.create(
        city=mentor.city,
        start_at=datetime(2022, 10, 1, 12, 0, 0, tzinfo=pytz.UTC)
    )
    event_november = factories.EventFactory.create(
        city=mentor.city,
        start_at=datetime(2022, 11, 1, 12, 0, 0, tzinfo=pytz.UTC)
    )
    url = reverse('events-months')
    response = mentor_client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 3
    for month_name in response.json():
        assert isinstance(month_name, str)

    assert event_september.start_at.strftime('%B') in response.json()
    assert event_october.start_at.strftime('%B') in response.json()
    assert event_november.start_at.strftime('%B') in response.json()


def test_archived_events_available(mentor, mentor_client):
    # not started events
    factories.EventFactory.create_batch(PAGE_SIZE + 1, city=mentor.city)

    # event in the past
    factories.EventFactory.create(
        city=mentor.city,
        start_at=datetime.now(tz=pytz.UTC) + timedelta(seconds=1),
        end_at=datetime.now(tz=pytz.UTC) + timedelta(seconds=3),
    )
    time.sleep(5)

    url = reverse('events-archive')
    response = mentor_client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert 'count' in data
    assert 'next' in data
    assert 'previous' in data
    assert 'results' in data
    assert type(data['results']) == list
    assert data['count'] == 1
    assert len(data['results']) == 1


def test_events_for_user_only_in_his_city(mentor, mentor_client):
    factories.EventFactory.create_batch(10)
    factories.EventFactory.create_batch(PAGE_SIZE - 1, city=mentor.city)
    url = reverse('events-list')
    response = mentor_client.get(url)

    assert response.status_code == 200
    assert len(response.json()['results']) == PAGE_SIZE - 1

