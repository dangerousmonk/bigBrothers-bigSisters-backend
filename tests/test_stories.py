import os
import shutil

from django.conf import settings
from django.urls import reverse

import pytest
from rest_framework.test import override_settings

from bbbs.story.models import Story

from . import factories
from .config import BASE_DIR

pytestmark = pytest.mark.django_db
PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')
TEMP_DIR = 'test_files'
URL_LIST = reverse('stories-list')


@override_settings(MEDIA_ROOT=TEMP_DIR)
def test_stories_list_endpoint_available(client):
    factories.StoryFactory.create_batch(PAGE_SIZE + 1)
    response = client.get(URL_LIST)
    response_data = response.json()

    assert response.status_code == 200
    assert 'count' in response_data
    assert 'next' in response_data
    assert 'previous' in response_data
    assert 'results' in response_data
    assert type(response_data['results']) == list
    assert response_data['count'] == PAGE_SIZE + 1
    assert len(response_data['results']) == PAGE_SIZE


@override_settings(MEDIA_ROOT=TEMP_DIR)
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
        'author': author['email'],
        'added_at': story.added_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'intro': story.intro,
        'text': story.text,
        'quote': story.quote,
        'image': story.image,
    }
    response = client.get(url)

    assert response.status_code == 200
    assert expected == response.json()


@override_settings(MEDIA_ROOT=TEMP_DIR)
def test_stories_create_endpoint_valid_data(mentor, mentor_client):
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
    response = mentor_client.post(URL_LIST, data=data, format='json')
    created = Story.objects.first()

    assert response.status_code == 201
    assert Story.objects.count() == num_stories + 1
    assert hasattr(created, 'author')
    assert created.author == mentor
    assert created.show_on_main == False


@override_settings(MEDIA_ROOT=TEMP_DIR)
def test_stories_create_endpoint_no_data(mentor_client):
    data = {}
    response = mentor_client.post(URL_LIST, data=data, format='json')
    assert response.status_code == 400


INVALID_SINCE_DATES = [
    '',
    '2029-01-01',
    '01-01-2021',
]


@override_settings(MEDIA_ROOT=TEMP_DIR)
@pytest.mark.parametrize('friends_since', INVALID_SINCE_DATES)
def test_stories_create_endpoint_invalid_data(mentor_client, friends_since):
    story = factories.StoryFactory.build()
    data = {
        'title': story.title,
        'child_name': story.child_name,
        'friends_since': friends_since,
        'intro': story.intro,
        'text': story.text,
        'quote': story.quote,
    }
    response = mentor_client.post(URL_LIST, data=data, format='json')
    assert response.status_code == 400


@override_settings(MEDIA_ROOT=TEMP_DIR)
def test_stories_update_endpoint(mentor, mentor_client):
    old_story = factories.StoryFactory.create(author=mentor)
    url = reverse('stories-detail', kwargs={'pk': old_story.id})
    story = factories.StoryFactory.build()
    mentor_info = mentor.__dict__

    expected_json = story.__dict__
    expected_json.pop('_state')
    expected_json.pop('author_id')
    expected_json.pop('modified_at')
    expected_json.pop('show_on_main')
    expected_json.pop('image')

    expected_json['author'] = mentor_info.pop('email')
    expected_json['id'] = old_story.id
    expected_json['added_at'] = old_story.added_at.strftime(
        '%Y-%m-%dT%H:%M:%S%z')
    expected_json['friends_since'] = story.friends_since.strftime(
        '%Y-%m-%d')

    response = mentor_client.put(url, expected_json, format='multipart')
    assert response.status_code == 200

    expected_json['image'] = old_story.image
    assert response.json() == expected_json


@override_settings(MEDIA_ROOT=TEMP_DIR)
def test_mentor_can_not_update_other_users_stories(mentor_client):
    story = factories.StoryFactory.create()
    url = reverse('stories-detail', kwargs={'pk': story.id})
    response = mentor_client.put(url, data={}, format='multipart')
    assert response.status_code == 403


FIELDS_TO_PATCH = [
    'title',
    'child_name',
    'friends_since',
    'intro',
    'text',
    'quote',
    'image'
]


@override_settings(MEDIA_ROOT=TEMP_DIR)
@pytest.mark.parametrize('field', FIELDS_TO_PATCH)
def test_stories_partial_update_endpoint(mentor, field, mentor_client):
    old_story = factories.StoryFactory.create(author=mentor)
    new_story = factories.StoryFactory.build()
    new_field_value = {
        field: new_story.__dict__[field]
    }
    url = reverse('stories-detail', kwargs={'pk': old_story.id})
    response = mentor_client.patch(url, data=new_field_value, format='multipart')
    assert response.status_code == 200


@override_settings(MEDIA_ROOT=TEMP_DIR)
def test_stories_destroy_endpoint_not_available(mentor, mentor_client):
    story = factories.StoryFactory.create(author=mentor)
    url = reverse('stories-detail', kwargs={'pk': story.id})
    response = mentor_client.delete(url)
    assert response.status_code == 405


def test_remove_temp_dir():
    try:
        shutil.rmtree(os.path.join(BASE_DIR, TEMP_DIR))
    except OSError as err:
        print(err)
