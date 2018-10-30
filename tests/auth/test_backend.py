import pytest
from django.conf import settings
from django.contrib.auth import authenticate

INTROSPECTION_URL = f"{settings.AUTHORIZATION_SERVER_URL}/o/introspect/"


def test_unauthorized_user(rf):
    """
    Test that authentication a request with no Authorization header
    does not return an authenticated user.
    """
    assert (
        authenticate(rf.post(INTROSPECTION_URL)) is None
    ), "user is authenticated without access token"


def test_invalid_token_request(rf, invalid_token_mock):
    """
    Test that a request with an Authorization header with an invalid token
    does not return an authenticated user.
    """
    assert (
        authenticate(
            rf.post(INTROSPECTION_URL, HTTP_AUTHORIZATION="Bearer invalid_token")
        )
        is None
    ), "user authenticated with invalid token"


def test_valid_token_request(rf, valid_token_mock):
    """
    Test that a request with an Authorization header with a valid token
    returns an authenticated user.
    """
    user = authenticate(
        rf.post(INTROSPECTION_URL, HTTP_AUTHORIZATION="Bearer valid_token")
    )
    assert user is not None, "authentication failed"


def test_unauthorized_backend(rf, unauthorized_request_mock):
    """
    Test that a request with a token does not return an authenticated user
    when the introspection token is invalid.
    """
    assert (
        authenticate(
            rf.post(INTROSPECTION_URL, HTTP_AUTHORIZATION="Bearer valid_token")
        )
        is None
    ), "user is authenticated without access to authorization server"
