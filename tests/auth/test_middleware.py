import pytest
from django.contrib.auth import authenticate
from django.urls import reverse

INTROSPECTION_URL = "https://dashit.win.tue.nl/o/introspect/"


@pytest.mark.django_db
def test_invalid_token_request(api_client, invalid_token_mock):
    response = api_client.get(
        reverse("coursera-api:course-list"), HTTP_AUTHORIZATION="Bearer invalid_token"
    )
    assert response.status_code == 403, "user authenticated with invalid token"


@pytest.mark.django_db
def test_valid_token_request(api_client, valid_token_mock):
    response = api_client.get(
        reverse("coursera-api:course-list"), HTTP_AUTHORIZATION="Bearer valid_token"
    )
    assert response.status_code == 200, "authentication failed"


@pytest.mark.django_db
def test_unauthorized_backend(teacher_api_client, invalid_token_mock):
    response = teacher_api_client.get(
        reverse("coursera-api:course-list"), HTTP_AUTHORIZATION="Bearer invalid_token"
    )
    assert response.status_code == 200, "authentication failed"
