import os

import pytest
from auth.users import User
from coursera.models import Course
from coursera_dashboard.db_router import DatabaseRouter
from django.conf import settings
from pytest_factoryboy import register
from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture
def coursera_course_id():
    return "27_khHs4EeaXRRKK7mMjqw"


@pytest.fixture
def coursera_course(coursera_course_id):
    return Course.objects.get(pk=coursera_course_id)


@pytest.fixture
def teacher(coursera_course_id):
    return User(
        username="teacher@dashit.win.tue.nl",
        active=True,
        scope="read write",
        role="teacher",
        courses=[coursera_course_id],
    )


@pytest.fixture
def teacher_api_client(teacher):
    client = APIClient()
    client.force_authenticate(teacher)
    return client


@pytest.fixture
def valid_token_mock(requests_mock, teacher):
    requests_mock.post(
        "https://dashit.win.tue.nl/o/introspect/",
        json={
            "username": teacher.username,
            "active": teacher.is_authenticated,
            "scope": "".join(teacher.scopes),
            "role": teacher.role,
            "courses": list(teacher.courses),
        },
    )


@pytest.fixture
def invalid_token_mock(requests_mock):
    requests_mock.post(
        "https://dashit.win.tue.nl/o/introspect/", json={"active": False}
    )


@pytest.fixture
def unauthorized_request_mock(requests_mock):
    requests_mock.post("https://dashit.win.tue.nl/o/introspect/", status_code=403)


@pytest.fixture
def rf():
    return APIRequestFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def db_router():
    return DatabaseRouter()
