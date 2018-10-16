import os

import pytest
from django.conf import settings
from pytest_factoryboy import register
from rest_framework.test import APIClient, APIRequestFactory

from auth.users import User
from coursera.models import Course
from coursera_dashboard.db_router import DatabaseRouter


@pytest.fixture
def coursera_course_id():
    return "27_khHs4EeaXRRKK7mMjqw"


@pytest.fixture
def coursera_video_id():
    return "jx3EZ"


@pytest.fixture
def coursera_assessment_base_id():
    return "xnoY2YyIEeaZmBK0AXp1hQ"


@pytest.fixture
def coursera_assessment_version():
    return "7"


@pytest.fixture
def coursera_assignment_id():
    return "hLatC"


@pytest.fixture
def coursera_assessment_id(coursera_assessment_base_id, coursera_assessment_version):
    return f"{coursera_assessment_base_id}@{coursera_assessment_version}"


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
        courses=[coursera_course_id, "oWawIRajEeWEjBINzvDOWw"],
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
