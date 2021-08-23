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


def test_participate_only_for_authorized(client):
    url = reverse('event-participants-list')
    response = client.get(url)
    assert response.status_code == 401


def test_mentor_can_register_for_event(mentor, mentor_client):
    participants_num = EventParticipant.objects.count()
    assert participants_num == 0

    event = factories.EventFactory.create(city=mentor.city)
    url = reverse('event-participants-list')
    data = {'event': event.id}
    response = mentor_client.post(url, data=data)

    assert response.status_code == 201
    assert EventParticipant.objects.count() == participants_num + 1


def test_mentor_can_not_register_twice(mentor, mentor_client):
    participants_num = EventParticipant.objects.count()
    assert participants_num == 0

    event = factories.EventFactory.create(city=mentor.city)
    url = reverse('event-participants-list')
    data = {'event': event.id}
    response = mentor_client.post(url, data=data)

    assert response.status_code == 201
    assert EventParticipant.objects.count() == participants_num + 1

    response = mentor_client.post(url, data=data)
    assert response.status_code == 400
    assert EventParticipant.objects.count() == participants_num + 1


def test_mentor_can_unregister():
    pass


def test_mentor_can_not_register_without_free_seats():
    pass
