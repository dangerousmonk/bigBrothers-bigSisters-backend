from django.conf import settings
from django.urls import reverse

import pytest
from . import factories

from bbbs.story.models import Story

pytestmark = pytest.mark.django_db
PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')


def test_stories_list_endpoint_available(client):
    url = reverse('stories-list')
    factories.StoryFactory.create_batch(PAGE_SIZE + 1)
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


def test_stories_detail_endpoint_available(client, mentor):
    story = factories.StoryFactory.create(author=mentor)
    url = reverse('stories-detail', kwargs={'pk': story.id})

    mentor_info = mentor.__dict__
    author = dict()
    author['id'] = mentor_info.pop('id')
    author['first_name'] = mentor_info.pop('first_name')
    author['last_name'] = mentor_info.pop('last_name')
    author['email'] = mentor_info.pop('email')

    expected = {
        'id': story.id,
        'title': story.title,
        'child_name': story.child_name,
        'friends_since': story.friends_since.strftime('%Y-%m-%d'),
        'author': author,
        'added_at': story.added_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'intro': story.intro,
        'text': story.text,
        'quote': story.quote,
        'image': story.image,
    }
    response = client.get(url)

    assert response.status_code == 200
    assert expected == response.json()



def test_stories_create_endpoint(mentor, mentor_client):
    url = reverse('stories-list')
    num_stories = Story.objects.count()
    story = factories.StoryFactory.build()
    data = {
        'title': story.title,
        'child_name': story.child_name,
        'friends_since': story.friends_since,
        'intro': story.intro,
        'text': story.text,
        'quote': story.quote,
    }
    response = mentor_client.post(url, data=data, format='json')
    assert response.status_code == 201




def test_stories_update_endpoint():
    pass

