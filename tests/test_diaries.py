from django.conf import settings
from django.urls import reverse

import pytest

from bbbs.diary.models import Diary

from . import factories

pytestmark = pytest.mark.django_db
PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')


class TestDiaryEndpoints:
    endpoint_list = reverse('diaries-list')

    def test_get_diary_list(self, client, mentor_client):
        response = client.get(self.endpoint_list)
        assert response.status_code == 401

        response = mentor_client.get(self.endpoint_list)
        assert response.status_code == 200

    def test_get_diary_list_with_pagination(self, mentor, mentor_client):
        factories.DiaryFactory.create_batch(PAGE_SIZE + 1, author=mentor)
        factories.DiaryFactory.create()

        response = mentor_client.get(self.endpoint_list)
        response_data = response.json()

        assert 'count' in response_data
        assert 'next' in response_data
        assert 'previous' in response_data
        assert 'results' in response_data, 'pagination is not set'

        assert type(response_data['results']) == list, 'results must be a list'
        assert response_data['count'] == PAGE_SIZE + 1, 'incorrect count value'
        assert len(response_data['results']) == PAGE_SIZE, 'incorrect results len'

    def test_get_diary_detail(self, client, mentor, mentor_client):
        mentor_diary = factories.DiaryFactory.create(author=mentor)
        diary = factories.DiaryFactory.create()

        url = reverse('diaries-detail', kwargs={'pk': mentor_diary.id})
        response = mentor_client.get(url)
        data = response.json()

        assert response.status_code == 200, 'must return 200 for diary owner'

        expected = {
            'id': mentor_diary.id,
            'place': mentor_diary.place,
            'meeting_date': mentor_diary.meeting_date.strftime('%Y-%m-%d'),
            'added_at': mentor_diary.added_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'modified_at': mentor_diary.modified_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'description': mentor_diary.description,
            'image': mentor_diary.image,
            'sent_to_curator': mentor_diary.sent_to_curator,
            'mark': mentor_diary.mark,
        }
        assert expected == data

        response = client.get(url)
        assert response.status_code == 401

        url = reverse('diaries-detail', kwargs={'pk': diary.id})
        response = mentor_client.get(url)

        assert response.status_code == 404  # TODO: restrict via permissions?

    def test_diary_post(self, mentor, mentor_client):
        num_diaries = Diary.objects.count()
        url = reverse('diaries-list')

        diary = factories.DiaryFactory.build()
        expected = {
            'place': diary.place,
            'meeting_date': diary.meeting_date.strftime('%Y-%m-%d'),
            'description': diary.description,
            'mark': diary.mark,
        }
        response = mentor_client.post(url, data=expected, format='json')
        created = Diary.objects.get(id=1)

        assert response.status_code == 201
        assert Diary.objects.count() == num_diaries + 1
        assert hasattr(created, 'author')
        assert created.author == mentor

        # author-meeting_date-place must be unique
        expected['description'] = 'brand new description'
        response = mentor_client.post(url, data=expected, format='json')
        assert response.status_code == 400

    INVALID_MEETING_DATES = [
        '',
        '2020-01-01',
        '2029-01-01',
        '01-01-2021',
        '12345'
    ]

    @pytest.mark.parametrize('meeting_date', INVALID_MEETING_DATES)
    def test_diary_post_with_invalid_meeting_date(self, mentor_client, meeting_date):
        url = reverse('diaries-list')
        diary = factories.DiaryFactory.build()
        expected = {
            'place': diary.place,
            'meeting_date': meeting_date,
            'description': diary.description,
            'mark': diary.mark,
        }

        response = mentor_client.post(url, data=expected, format='json')
        assert response.status_code == 400

    INVALID_PLACE = [
        '',
        'a',
        'a' * 101,
    ]

    @pytest.mark.parametrize('place', INVALID_PLACE)
    def test_diary_post_with_invalid_place(self, mentor_client, place):
        url = reverse('diaries-list')
        diary = factories.DiaryFactory.build()
        data = {
            'place': place,
            'meeting_date': diary.meeting_date.strftime('%Y-%m-%d'),
            'description': diary.description,
            'mark': diary.mark,
        }

        response = mentor_client.post(url, data=data, format='json')
        assert response.status_code == 400

    def test_diary_update(self, mentor, mentor_client):
        old_diary = factories.DiaryFactory.create(author=mentor)
        new_diary = factories.DiaryFactory.build()
        expected_json = {
            'place': new_diary.place,
            'meeting_date': new_diary.meeting_date.strftime('%Y-%m-%d'),
            'description': new_diary.description,
            'mark': new_diary.mark,
            #'image': new_diary.image,
        }

        url = reverse('diaries-detail', kwargs={'pk': old_diary.id})
        response = mentor_client.put(url, expected_json, format='json')
        expected_json['id'] = old_diary.id
        expected_json['sent_to_curator'] = old_diary.sent_to_curator
        expected_json['added_at'] = old_diary.added_at.strftime(
            '%Y-%m-%dT%H:%M:%S%z')
        # Note: build() is used, no save(), fix later
        expected_json['modified_at'] = old_diary.modified_at.strftime(
            '%Y-%m-%dT%H:%M:%S%z')
        expected_json['image'] = old_diary.image
        assert response.status_code == 200
        assert response.json() == expected_json

    FIELDS = [
        'place',
        'meeting_date',
        'description',
        'mark'
    ]

    @pytest.mark.parametrize('field', FIELDS)
    def test_diary_partial_update(self, field, mentor, mentor_client):
        old_diary = factories.DiaryFactory.create(author=mentor)

        new_diary = factories.DiaryFactory.build()
        url = reverse('diaries-detail', kwargs={'pk': old_diary.id})

        valid_field = {field: new_diary.__dict__[field]}
        if field == 'meeting_date':
            valid_field = {field: new_diary.__dict__[field].strftime('%Y-%m-%d')}
        response = mentor_client.patch(url, valid_field, format='json')

        assert response.status_code == 200 or response.status_code == 301
        assert response.json()[field] == valid_field[field]

    def test_diary_delete(self, mentor, mentor_client):
        diary = factories.DiaryFactory.create(author=mentor)
        diary2 = factories.DiaryFactory.create()

        url = reverse('diaries-detail', kwargs={'pk': diary2.id})
        response = mentor_client.delete(url)
        assert response.status_code == 404  # TODO: throw permissions error instead of 404

        url = reverse('diaries-detail', kwargs={'pk': diary.id})
        response = mentor_client.delete(url)
        assert response.status_code == 204 or response.status_code == 301
