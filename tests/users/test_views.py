import json
from urllib.parse import urlparse

import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from oauth2_provider.models import Application, Grant

from users.models import User


@pytest.mark.django_db
def test_test_view(user_api_client):
    response = user_api_client.get(reverse("users-api:test-view"))
    assert response.status_code == 200, "could not reach test view"
    assert json.loads(response.content) == {
        "success": "You have a valid access token"
    }, "response returned unexpected data"


@pytest.mark.django_db
def test_test_view_no_access(api_client):
    response = api_client.get(reverse("users-api:test-view"))
    assert response.status_code == 403, "unauthenticated user could reach test view"


@pytest.mark.django_db
def test_login_template(client):
    response = client.get(reverse("users:login"))
    assert "registration/login.html" in [
        t.name for t in response.templates if t.name is not None
    ], "did not use correct template"


@pytest.mark.django_db
def test_user_viewset_must_be_admin(user_api_client):
    response = user_api_client.get(reverse("users-api:user-list"))
    assert response.status_code == 403, "regular user has permission"


@pytest.mark.django_db
def test_admin_can_access_user_viewset(admin_api_client):
    response = admin_api_client.get(reverse("users-api:user-list"))
    assert response.status_code == 200, "admin user has no permission"


@pytest.mark.django_db
def test_user_viewset_detail(admin_api_client, user):
    response = admin_api_client.get(
        reverse("users-api:user-detail", kwargs={"pk": user.pk})
    )
    assert response.status_code == 200, "admin user can't view user details"
    assert response.data == {
        "email": "john.doe@example.com"
    }, "response returned unexpected data"


@pytest.mark.django_db
def test_user_viewset_create(admin_api_client):
    response = admin_api_client.post(
        reverse("users-api:user-list"), {"email": "new@example.com"}
    )
    assert response.status_code == 201, "could not create new user"
    assert response.data == {
        "email": "new@example.com"
    }, "response returned unexpected data"
    user = User.objects.get(email="new@example.com")
    assert user.is_active, "new user is not active"


@pytest.mark.django_db
def test_create_user_send_email(admin_api_client, mailoutbox):
    admin_api_client.post(reverse("users-api:user-list"), {"email": "new@example.com"})
    assert len(mailoutbox) == 1, "no mails sent"
    m = mailoutbox[0]
    assert m.subject == "An account has been created", "subject does not match"
    assert list(m.to) == ["new@example.com"], "to address does not match"


@pytest.mark.django_db
def test_reset_password(user, api_client):
    token = default_token_generator.make_token(user)
    response = api_client.put(
        reverse("users-api:user-password-reset", kwargs={"pk": user.pk}),
        {"token": token, "password": "7jz*X6CkMH9s&hEEEF9%QrQ^"},
    )
    assert response.status_code == 200, "could not reset password"
    user.refresh_from_db()
    assert user.check_password(
        "7jz*X6CkMH9s&hEEEF9%QrQ^"
    ), "password was not set correctly"


@pytest.mark.django_db
def test_reset_password_low_quality_password(user, api_client):
    token = default_token_generator.make_token(user)
    response = api_client.put(
        reverse("users-api:user-password-reset", kwargs={"pk": user.pk}),
        {"token": token, "password": "password"},
    )
    assert response.status_code == 400, "request with low-quality password succeeded"
    assert response.data == {
        "password": ["This password is too common."]
    }, "response returned unexpected data"


@pytest.mark.django_db
def test_reset_password_invalid_token(user, api_client):
    response = api_client.put(
        reverse("users-api:user-password-reset", kwargs={"pk": user.pk}),
        {"token": "invalid_token", "password": "new_password"},
    )
    assert response.status_code == 400, "request with invalid token succeeded"
    assert response.data == {
        "token": ["Invalid password reset token."]
    }, "response returned unexpected data"


@pytest.mark.django_db
def test_authorize(api_client, user):
    application = Application.objects.get(name="DASH-IT Frontend")

    response = api_client.post(
        reverse("oauth2_provider:token"),
        {
            "client_id": application.client_id,
            "grant_type": Application.GRANT_PASSWORD,
            "username": user.email,
            "password": "password",
        },
    )
    assert response.status_code == 200, "failed to log in"
    data = json.loads(response.content)
    assert "access_token" in data, "did not recieve access token"
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {data['access_token']}")
    test_response = api_client.get(reverse("users-api:test-view"))
    assert test_response.status_code == 200, "could not access test view"
