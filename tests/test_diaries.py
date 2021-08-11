# Test Case Description
# Test endpoint is available only for authorized clients - DONE
# Test list endpoint  returns paginated results - DONE
# Test mentor can submit new diary via endpoint - DONE
# Test mentor can update his diary
# Test mentor can delete his own diary
# Test mentor can not delete another mentors diary
# Test mentor can send his diary to curators

import pytest
from django.urls import reverse
from django.conf import settings
from . import factories
from bbbs.diary.models import Diary

pytestmark = pytest.mark.django_db
PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')


class TestDiaryEndpoints:
    endpoint_list = reverse('diaries-list')

    def test_get_diary_list(self, client, mentor_client):
        response = client.get(self.endpoint_list)
        assert response.status_code == 401, 'for unauthorized clients must return 401'

        response = mentor_client.get(self.endpoint_list)
        assert response.status_code == 200, 'for authorized clients must return 200'

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
            'image': None,  # TODO: test image
            'sent_to_curator': mentor_diary.sent_to_curator,
            'mark': mentor_diary.mark,
        }
        assert expected == data, 'must return correct data/data format'

        response = client.get(url)
        assert response.status_code == 401, 'must return 401 for unauthorized'

        url = reverse('diaries-detail', kwargs={'pk': diary.id})
        response = mentor_client.get(url)

        assert response.status_code == 404, 'must return 404 for not mentors diary'  # TODO: restrict via permissions?

    INVALID_DATES = [
        '',
        '2020-01-01',
        '2029-01-01',
        '01-01-2021',
        '12345'
    ]

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

        expected['description'] = 'brand new description'
        response = mentor_client.post(url, data=expected, format='json')
        assert response.status_code == 400

    @pytest.mark.parametrize('meeting_date', INVALID_DATES)
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

    def test_diary_update(self, mentor, mentor_client):
        old_diary = factories.DiaryFactory.create(author=mentor)
        new_diary = factories.DiaryFactory.build()
        expected = {
            'id': new_diary.id,
            'place': new_diary.place,
            'meeting_date': new_diary.meeting_date.strftime('%Y-%m-%d'),
            'description': new_diary.description,
            'image': None,  # TODO: test image
            'sent_to_curator': new_diary.sent_to_curator,
            'mark': new_diary.mark,
        }
        url = reverse('diaries-detail', kwargs={'pk':old_diary.id})
        response = mentor_client.put(url, expected, format='json')
        assert response.status_code == 200
        assert response.json() == expected

