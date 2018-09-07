import pytest

from users.models import User


@pytest.mark.django_db
def test_can_create_user():
    user = User.objects.create_user("test_user", "test_user@example.com", "password")
