import pytest
from oauth2_provider.models import Application

from users.models import User


@pytest.mark.django_db
def test_can_create_user():
    user = User.objects.create_user("test_user", "test_user@example.com", "password")
    assert user.username == "test_user", "username is set incorrectly"
    assert user.email == "test_user@example.com", "email is set incorrectly"
    assert user.check_password("password"), "password is set incorreclty"


@pytest.mark.django_db
def test_user_can_login(user):
    assert user.check_password("password"), "password is incorrect"


@pytest.mark.django_db
def test_application_exists():
    assert Application.objects.exists(), "application is not created"
