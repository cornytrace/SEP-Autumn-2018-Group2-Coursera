import pytest
from django.contrib.auth import authenticate

INTROSPECTION_URL = "https://dashit.win.tue.nl/o/introspect/"


def test_unauthorized_user(rf):
    assert (
        authenticate(rf.post(INTROSPECTION_URL)) is None
    ), "user is authenticated without access token"


def test_invalid_token_request(rf, invalid_token_mock):
    assert (
        authenticate(
            rf.post(INTROSPECTION_URL, HTTP_AUTHORIZATION="Bearer invalid_token")
        )
        is None
    ), "user authenticated with invalid token"


def test_valid_token_request(rf, valid_token_mock):
    user = authenticate(
        rf.post(INTROSPECTION_URL, HTTP_AUTHORIZATION="Bearer valid_token")
    )
    assert user is not None, "authentication failed"


def test_unauthorized_backend(rf, unauthorized_request_mock):
    assert (
        authenticate(
            rf.post(INTROSPECTION_URL, HTTP_AUTHORIZATION="Bearer valid_token")
        )
        is None
    ), "user is authenticated without access to authorization server"
