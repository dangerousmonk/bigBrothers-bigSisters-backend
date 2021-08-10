# Test Case Description
# Test endpoint is available only for authorized clients - DONE
# Test list endpoint  returns paginated results - DONE
# Test mentor can submit new diary via endpoint
# Test mentor can update his diary
# Test mentor can delete his own diary
# Test mentor can not delete another mentors diary
# Test mentor can send his diary to curators

import pytest
from django.urls import reverse
from django.conf import settings
from . import factories

pytestmark = pytest.mark.django_db


class TestDiaryEndpoints:
    endpoint_list = reverse('diaries-list')
    PAGE_SIZE = settings.REST_FRAMEWORK.get('PAGE_SIZE')

    def test_endpoint_list(self, client, mentor, mentor_client):
        factories.DiaryFactory.create_batch(self.PAGE_SIZE+1, author=mentor)
        factories.DiaryFactory.create()

        response = client.get(self.endpoint_list)
        assert response.status_code == 401, f'{self.endpoint_list} must return 401 for unauthorized'
        response = mentor_client.get(self.endpoint_list)
        assert response.status_code == 200, f'{self.endpoint_list} must return 200 for authorized'

        response_data = response.json()
        assert 'count' in response_data
        assert 'next' in response_data
        assert 'previous' in response_data
        assert 'results' in response_data, f'{self.endpoint_list} returned data without pagination'

        assert type(response_data['results']) == list, (
            f'{self.endpoint_list} returned incorrect data type for results parameter'
        )
        assert response_data['count'] == self.PAGE_SIZE+1, (
            f'{self.endpoint_list} returned incorrect count value')
        assert len(response_data['results']) == self.PAGE_SIZE, (
            f'{self.endpoint_list} returned incorrect results value')