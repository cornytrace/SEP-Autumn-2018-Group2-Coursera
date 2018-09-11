import pytest
from oauth2_provider.models import Application

from users.models import User


def test_email_is_username():
    assert User.USERNAME_FIELD == "email", "USERNAME_FIELD is not correct"


@pytest.mark.django_db
def test_can_create_user():
    user = User.objects.create_user("test_user@example.com", "password")
    assert user.email == "test_user@example.com", "email is set incorrectly"
    assert user.check_password("password"), "password is set incorreclty"


@pytest.mark.django_db
def test_can_create_superuser():
    user = User.objects.create_superuser("admin@example.com", "password")
    assert user.is_superuser, "user is not a superuser"


@pytest.mark.django_db
def test_superuser_must_be_staff():
    with pytest.raises(ValueError):
        User.objects.create_superuser("admin@example.com", "password", is_staff=False)


@pytest.mark.django_db
def test_superuser_must_be_superuser():
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            "admin@example.com", "password", is_superuser=False
        )


@pytest.mark.django_db
def test_user_can_login(user):
    assert user.check_password("password"), "password is incorrect"


@pytest.mark.django_db
def test_application_exists():
    assert Application.objects.exists(), "application is not created"
