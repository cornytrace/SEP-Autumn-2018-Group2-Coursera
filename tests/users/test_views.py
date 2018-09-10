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
def test_authorize(client, user):
    application = Application.objects.get(name="DASH-IT Frontend")
    application.redirect_uris = "http://localhost:8080/"
    application.save()

    client.force_login(user)
    response = client.get(
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
