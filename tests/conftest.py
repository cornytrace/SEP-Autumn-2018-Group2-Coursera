import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from users.models import User

from .courses.factories import CourseFactory
from .users.factories import AccessTokenFactory, UserFactory

register(UserFactory)
register(
    UserFactory,
    "admin",
    email="admin@example.com",
    role=User.ADMIN,
    is_staff=True,
    is_superuser=True,
)
register(UserFactory, "teacher", email="teacher@example.com", role=User.TEACHER)
register(UserFactory, "qdt", email="qdt@example.com", role=User.QDT)
register(CourseFactory)


@pytest.fixture
def user_access_token(user):
    return AccessTokenFactory(user=user)


@pytest.fixture
def admin_access_token(admin):
    return AccessTokenFactory(user=admin)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_api_client(user_access_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_access_token}")
    return client


@pytest.fixture
def admin_api_client(admin_access_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_access_token}")
    return client
