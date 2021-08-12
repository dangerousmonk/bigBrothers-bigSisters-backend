import pytest
from django.urls import reverse
from . import factories

pytestmark = pytest.mark.django_db


def test_rights_list_endpoint_available(client):
    assert False