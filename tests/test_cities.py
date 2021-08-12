import pytest
from django.urls import reverse
from . import factories

pytestmark = pytest.mark.django_db


def test_cities_list_endpoint_available(client):
    factories.CityFactory.create_batch(10)
    url = reverse('cities-list')
    response = client.get(url)
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 10


def test_city_detail_endpoint_available(client):
    city = factories.CityFactory.create()
    url = reverse('cities-detail', kwargs={'pk': city.id})
    expected = {
        'id': city.id,
        'name': city.name,
        'is_primary': city.is_primary,
    }
    response = client.get(url)

    assert response.status_code == 200
    assert expected == response.json()


def test_cities_endpoint_read_only(mentor_client):
    city = factories.CityFactory.build()
    url_list = reverse('cities-list')
    url_detail = reverse('cities-detail', kwargs={'pk': city.id})

    response = mentor_client.post(url_list, data={})
    assert response.status_code == 405

    response = mentor_client.patch(url_detail, data={})
    assert response.status_code == 405

    response = mentor_client.delete(url_detail)
    assert response.status_code == 405
