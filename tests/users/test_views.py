from urllib.parse import urlparse

import pytest
from django.urls import reverse
from oauth2_provider.models import Application, Grant


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


@pytest.mark.django_db
def test_authorize(user_api_client):
    application = Application.objects.get(name="DASH-IT Frontend")
    application.redirect_uris = "http://localhost:8080/"
    application.save()

    response = user_api_client.get(
        reverse("oauth2_provider:authorize")
        + "?client_id="
        + application.client_id
        + "&state=random_state_string&response_type=code"
    )
    assert response.status_code == 302, "failed to get url"
    url = urlparse(response.url)
    assert url.scheme == "http", "wrong scheme"
    assert url.netloc == "localhost:8080", "wrong netloc"
    assert url.path == "/", "wrong path"
    assert "code" in url.query, "couldn't find 'code' in query"
