import pytest
from . import factories
from bbbs.common.choices import UserRoleChoices

@pytest.fixture
def mentor():
    curator = factories.UserFactory.create(role=UserRoleChoices.CURATOR)
    mentor = factories.UserFactory.create(role=UserRoleChoices.MENTOR, curator=curator)
    return mentor



@pytest.fixture
def token_for_mentor(mentor):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(mentor)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.fixture
def mentor_client(token_for_mentor):
    from rest_framework.test import APIClient
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_for_mentor["access"]}')
    return client
