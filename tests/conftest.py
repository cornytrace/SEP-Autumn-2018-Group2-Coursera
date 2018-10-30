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
    """
    Return the main course id used in the tests.
    """
    return "27_khHs4EeaXRRKK7mMjqw"


@pytest.fixture
def coursera_alt_course_id():
    """
    Return the alternate course id used in the tests.
    """
    return "oWawIRajEeWEjBINzvDOWw"


@pytest.fixture
def coursera_video_id():
    """
    Return the main video id used in the tests.
    """
    return "jx3EZ"


@pytest.fixture
def coursera_assessment_base_id():
    """
    Return the main assessment base id used in the tests.
    """
    return "xnoY2YyIEeaZmBK0AXp1hQ"


@pytest.fixture
def coursera_assessment_version():
    """
    Return the main version for coursera_assessment_base_id used in the tests.
    """
    return "7"


@pytest.fixture
def coursera_assignment_id():
    """
    Return the main assignment id used in the tests.
    """
    return "hLatC"


@pytest.fixture
def coursera_assessment_id(coursera_assessment_base_id, coursera_assessment_version):
    """
    Return the main assessment id used in the tests. Combines the assessment
    base id and assessment version.
    """
    return f"{coursera_assessment_base_id}@{coursera_assessment_version}"


@pytest.fixture
def coursera_course(coursera_course_id):
    """
    Return the main Course instance used in the tests.
    """
    return Course.objects.get(pk=coursera_course_id)


@pytest.fixture
def teacher(coursera_course_id):
    """
    Return an active user of type teacher with access to three of the main
    courses.
    """
    return User(
        username="teacher@dashit.win.tue.nl",
        active=True,
        scope="read write",
        role="teacher",
        courses=[
            coursera_course_id,
            "oWawIRajEeWEjBINzvDOWw",
            "V4m7Xf5qEeS9ISIACxWDhA",
        ],
    )


@pytest.fixture
def teacher_api_client(teacher):
    """
    Return a test API client authenticated as the teacher user.

    This client can be used to generate HTTP requests within the test suite.
    """
    client = APIClient()
    client.force_authenticate(teacher)
    return client


@pytest.fixture
def valid_token_mock(requests_mock, teacher):
    """
    Mock the authorization server introspection url to successfully validate
    the token.
    """
    requests_mock.post(
        f"{settings.AUTHORIZATION_SERVER_URL}/o/introspect/",
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
    """
    Mock the authorization server introspection url to reject the token.
    """
    requests_mock.post(
        f"{settings.AUTHORIZATION_SERVER_URL}/o/introspect/", json={"active": False}
    )


@pytest.fixture
def unauthorized_request_mock(requests_mock):
    """
    Mock the authorization server introspection url to reject the resource
    server's credentials.
    """
    requests_mock.post(
        f"{settings.AUTHORIZATION_SERVER_URL}/o/introspect/", status_code=403
    )


@pytest.fixture
def rf():
    """
    Return a request factory to create requests within the test suite.
    """
    return APIRequestFactory()


@pytest.fixture
def api_client():
    """
    Return a generic API client to generate HTTP requests.
    """
    return APIClient()


@pytest.fixture
def db_router():
    """
    Return a new DatabaseRouter instance.
    """
    return DatabaseRouter()
